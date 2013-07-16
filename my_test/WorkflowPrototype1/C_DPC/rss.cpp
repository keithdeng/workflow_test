#include <vector>
#include <cmath>
#include <iostream>
#include <complex>
#include <gsl_vector.h>
using namespace std;

double rss(const gsl_vector *params, void *variables ){

	double a0=gsl_vector_get(params, 0);
	double x1=gsl_vector_get(params, 1);
	complex<double> i(0.0,1.0);
	complex<double> *p = (complex<double> *) variables;
	int size = real(p[0]);
	vector<complex<double> > Fittedcurve(size);
	complex<double> temp;
	double rss=0.0;

	for (int j=0; j<size; ++j){
		Fittedcurve[j] = a0*p[j+1]*exp(i*x1*(j+1-(floor(size/2.0)+1)));
		temp = Fittedcurve[j] - p[j+size+1];
		rss += pow(abs(temp),2);
	}
	return rss;
	free(p);
}
