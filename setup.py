#!/usr/bin/env python
import builtins
import sys
from setuptools import setup, find_packages, Extension  # This setup relies on setuptools since distutils is insufficient and badly hacked code
from setuptools.command.build_ext import build_ext as _build_ext
import numpy

extensions = [
    Extension(
        name="pylandau",  # The module name you import
        sources=[
            "pyLandau/cpp/pylandau.pyx",     # Your Cython file (renamed from .cpp to .pyx?)
            "pyLandau/cpp/pylandau_src.cpp", # Your C++ implementation
        ],
        include_dirs=[
            numpy.get_include(),             # NumPy headers
            "pyLandau/cpp",                  # Your custom headers
        ],
        language="c++",
        extra_compile_args=["-std=c++11"],
    )
]

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        builtins.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

# Determine platform-specific compiler flags
extra_compile_args = ["-std=c++11"]  # Or use -std=c++17 if you like
extra_link_args = []

if sys.platform == "darwin":  # macOS-specific
    extra_compile_args += ["-stdlib=libc++"]
    extra_link_args += ["-stdlib=libc++"]


# Check if cython exists, then use it. Otherwise compile already cythonized cpp file
have_cython = False
try:
    from Cython.Build import cythonize
    have_cython = True
except ImportError:
    pass

if have_cython:
    cpp_extension = cythonize(Extension('pylandau', ['pyLandau/cpp/pylandau.pyx'],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,))
else:
    cpp_extension = [Extension('pylandau',
                               sources=['pyLandau/cpp/pylandau.cpp'],
                               language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,)]

install_requires = ['cython>=0.29', 'numpy>=1.21']

setup(
    cmdclass={'build_ext': build_ext},
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,  # accept all data files and directories matched by MANIFEST.in or found in source control
    package_data={'': ['README.*', 'VERSION'], 'docs': ['*'], 'examples': ['*']},
    ext_modules=cpp_extension,
    keywords=['Landau', 'Langau', 'PDF'],
    platforms='any'
)
