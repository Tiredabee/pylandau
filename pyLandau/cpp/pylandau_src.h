#ifndef PYLANDAU_SRC_H
#define PYLANDAU_SRC_H

double * getLandauPDFData(double * data, const unsigned int size, const double mu, const double eta);
double * getLangauPDFData(double * data, const unsigned int size, const double mu, const double eta, const double sigma);
double landauPDF(const double x, const double xi, const double x0);
double landauGaussPDF(const double x, const double mu, const double eta, const double sigma);
double gaussPDF(const double x, const double mu, const double sigma);

#endif // PYLANDAU_SRC_H
