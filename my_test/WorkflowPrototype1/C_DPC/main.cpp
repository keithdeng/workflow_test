/*  Computational Science Center, Brookhaven National Lab  *
 *  Cheng Chang                                            *
 *  Last modified on 05/31/2013                            */

#include <opencv2/opencv.hpp>
#include <complex>
#include "fftw3.h"
#include <stdio.h>
#include <vector>
#include <iostream>
#include <string>

#include <cstdio>

#include <limits>

#include <algorithm>

#include <iterator>

#include <cmath>
#include <gsl_sf.h>
#include "gsl_multimin.h"
#include <gsl_vector.h>
#include <time.h>
//#include <windows.h>

using namespace cv;
using namespace std;

extern IplImage* Loadtimepix(IplImage* LoadedImage);
extern double rss(const gsl_vector *params, void *variables);

int main( ){   
	
	clock_t start_time, finish_time;
	double runtime;
	start_time = clock();
	//LARGE_INTEGER freq, cnt1, cnt2;
	//QueryPerformanceFrequency(&freq);  //get the timer frequency
    //QueryPerformanceCounter(&cnt1);  //get the intital value of the timer

	cout.precision(16);
    const int reference_start = 1;
	const int row = 121;
	const int column = 121;
	const int p = 55;	
	const double pi = 3.141592653589793238462;
	const double energy = 19.5;
	const double lambda = (12.4/energy)*1e-4;  
	const double dx = 0.1;
	const double dy = 0.1;
	const double L = 1.46e6;	
	double ref_total = 0.0;
	int frame_num = 0;
	int kk = 0;
	const char det[20] = "Pilatus";
	char data_dir[100] = "/Users/admin/Documents/SOFC/SOFC_";
	char frame_num_char[20] = " ";

    IplImage *LoadedImage = 0; 
	IplImage *frame = 0;
	IplImage *temp = 0;

	for (int i = 1; i<=1; i++){
		for (int j = 1; j<=1; j++){
			frame_num = reference_start + kk;
			sprintf (frame_num_char, "%05d.tif", frame_num);
			strcat (data_dir, frame_num_char);		
		    LoadedImage = cvLoadImage(data_dir,	CV_64FC1);  //data_dir: image path, including image name
			if (!LoadedImage) printf ( "Could not load the image\n" );
	        
			kk+=1;

			if (i==1 && j==1){
				if (!strcmp(det, "Pilatus"))
					frame = cvCloneImage(LoadedImage);
				else if (!strcmp(det, "Timepix"))
					frame = Loadtimepix(LoadedImage);
				//cvSetImageROI( frame, rect_roi );
			}
			else{
				if (!strcmp( det,"Pilatus"))
					temp = cvCloneImage (LoadedImage);
				else if (!strcmp(det, "Timepix"))
					temp = Loadtimepix(LoadedImage);
				//cvSetImageROI( temp, rect_roi );
				frame = cvCloneImage(temp);  // assume only one reference!!!
			}
		}
	}

	CvMat* reference = cvCreateMat(61, 91, CV_64FC1);
    cvConvert(frame, reference);

	double *reference_ptr = reference->data.db;
	for (int i=0; i<reference->rows; i++){
		for (int j=0; j<reference->cols; j++){
			ref_total += (reference_ptr+i*91)[j];//ref_total is the same as MATLAB
		}
	}

	/*** Differential phase in x and y direction ***/
	const int step = reference->step/sizeof( double );   // equal num of clos
	const int start = 1;
	const int dim[2] = {reference->rows, reference->cols};

	double xline1[91] = {0.0};   
	double yline1_temp[61] = {0.0};
	double yline1 [15] = {0.0};
	
	for ( int i=0; i<reference->cols; i++ ){
		for ( int j=0; j<reference->rows; j++){
			xline1[i]+= (reference_ptr + j*step)[i];
		}
	}
	
	for ( int i=0; i<reference->rows; i++ ){
		for ( int j=0; j<reference->cols; j++){
			yline1_temp[i]+= (reference_ptr + i*step)[j];  
		}
	}

	for (int i=0; i<15; i++)
		yline1[i] = yline1_temp[i+46];   //xline1 and yline1 are the same as MATLAB

	/*** IFFT of xline1 and yline1 ***/
	fftw_complex *in_x1;
	fftw_complex *in_y1;
	fftw_complex *in_x2;
	fftw_complex *in_y2;
	fftw_complex *fx1_temp;
	fftw_complex *fy1_temp;
	fftw_complex *fx2_temp;
	fftw_complex *fy2_temp;

	vector<complex<double> > fx1;
	vector<complex<double> > fy1;

	fftw_plan plan_ifft_x1;
	fftw_plan plan_ifft_y1;

	in_x1    = (fftw_complex*) fftw_malloc( sizeof ( fftw_complex ) * reference->cols );
	in_y1    = (fftw_complex*) fftw_malloc( sizeof ( fftw_complex ) * 15 ); // 15 is the number of elements in yline1
	in_x2    = (fftw_complex*) fftw_malloc( sizeof ( fftw_complex ) * reference->cols );
	in_y2    = (fftw_complex*) fftw_malloc( sizeof ( fftw_complex ) * 15 ); // 15 is the number of elements in yline1
	fx1_temp = (fftw_complex*) fftw_malloc( sizeof ( fftw_complex ) * reference->cols );
	fy1_temp = (fftw_complex*) fftw_malloc( sizeof ( fftw_complex ) * 15 );
	fx2_temp = (fftw_complex*) fftw_malloc( sizeof ( fftw_complex ) * reference->cols );
	fy2_temp = (fftw_complex*) fftw_malloc( sizeof ( fftw_complex ) * 15 );

	plan_ifft_x1 = fftw_plan_dft_1d( reference->cols, in_x1, fx1_temp, FFTW_BACKWARD, FFTW_ESTIMATE );  // FFTW_PATIENT might be even faster
	plan_ifft_y1 = fftw_plan_dft_1d( 15, in_y1, fy1_temp, FFTW_BACKWARD, FFTW_ESTIMATE );

	for ( int i=0; i<reference->cols; i++){
		in_x1[i][0] = xline1[i];
		in_x1[i][1] = 0.0;
	}
	for ( int i=0; i<15; i++){
		in_y1[i][0] = yline1[i];
		in_y1[i][1] = 0.0;
	}

	fftw_execute(plan_ifft_x1); // fx1 is excuted WITHOUT FFTshift, fx1 is 91 times bigger than the true value !
    fftw_execute(plan_ifft_y1); // fy1 is excuted WITHOUT FFTshift, fy1 is 15 times bigger than the true value !

	//fftshift for fy1: same as MATLAB
	for ( int i=0; i<7; i++){
		complex<double> fy1_add (fy1_temp[i+8][0]/15.0, fy1_temp[i+8][1]/15.0);
		fy1.push_back(fy1_add);
	}
	for ( int i=7; i<15; i++){ 
		complex<double> fy1_add (fy1_temp[i-7][0]/15.0, fy1_temp[i-7][1]/15.0);
		fy1.push_back(fy1_add);
	}
	//fftshift for fx1: same as MATLAB
	for ( int i=0; i<45; i++){
		complex<double> fx1_add (fx1_temp[i+46][0]/91.0,fx1_temp[i+46][1]/91.0);
		fx1.push_back(fx1_add);
	}
	for ( int i=45; i<91; i++){
		complex<double> fx1_add (fx1_temp[i-45][0]/91.0,fx1_temp[i-45][1]/91.0);
		fx1.push_back(fx1_add);
	}

	//////////////////-----------non-linear fitting------------////////////////////
	double gx[121][121] = {0.0};
	double gy[121][121] = {0.0};
	double a[121][121]  = {0.0};

	vector<complex<double> > fx2;
	vector<complex<double> > fy2;
	vector<complex<double> > fx;
	vector<complex<double> > fy;
	double xline2[91]      = { 0.0 };              
	double yline2_temp[61] = { 0.0 };
	double yline2 [15]     = { 0.0 };
    double aa=0.0;
	const size_t np = 2;

	const gsl_multimin_fminimizer_type *T = gsl_multimin_fminimizer_nmsimplex;
	// Initial vertex size vector 				
	gsl_vector *ss;
	ss = gsl_vector_alloc (np);

	gsl_vector *x;
	x = gsl_vector_alloc (np);

	gsl_multimin_fminimizer *s = NULL;
	s = gsl_multimin_fminimizer_alloc (T, np); 

	gsl_multimin_function minex_func;
	size_t iter = 0;
    char data_dir_2[40];
	int ii=0, jj=0;
	fftw_plan plan_ifft_x2;
    fftw_plan plan_ifft_y2;

	for (int i=0; i<row; i++){
		for (int j=0; j<column; j++){		
			strcpy(data_dir_2, "/Users/admin/Documents/SOFC/SOFC_");
			frame_num = start + i*column + j;
			sprintf (frame_num_char, "%05d.tif", frame_num);
			strcat (data_dir_2, frame_num_char);		
            LoadedImage = cvLoadImage(data_dir_2, CV_64FC1);  //data_dir_2: image path, including image name		
			if ( !LoadedImage ) 
				printf ( "Could not load the image\n" ); //gx and gy have already been initialized as 0.0
			else{
				cvConvert( LoadedImage, reference );
				reference_ptr= reference->data.db;
				for ( ii=0; ii<reference->cols; ii++ ){
					for ( jj=0; jj<reference->rows; jj++){
						aa+= (reference_ptr + jj*step)[ii];												
					}
					xline2[ii]=aa;
					aa=0.0;
				}
				
				for ( ii=0; ii<reference->rows; ii++ ){
					for ( jj=0; jj<reference->cols; jj++){
						aa+= (reference_ptr + ii*step)[jj];  				
					}
					yline2_temp[ii]=aa;
					aa=0.0;
				}
				for (ii=0; ii<15; ii++)
					yline2[ii] = yline2_temp[ii+46];   //xline2 and yline2 are the same as MATLAB

				plan_ifft_x2 = fftw_plan_dft_1d( reference->cols, in_x2, fx2_temp, FFTW_BACKWARD, FFTW_ESTIMATE );  // FFTW_PATIENT might be even faster
	            plan_ifft_y2 = fftw_plan_dft_1d( 15, in_y2, fy2_temp, FFTW_BACKWARD, FFTW_ESTIMATE );

				for ( ii=0; ii<reference->cols; ii++){
					in_x2[ii][0] = xline2[ii];
					in_x2[ii][1] = 0.0;
				}
				for ( ii=0; ii<15; ii++){
					in_y2[ii][0] = yline2[ii];
					in_y2[ii][1] = 0.0;
				}

				fftw_execute(plan_ifft_x2); 
				fftw_execute(plan_ifft_y2);

				//fftshift for fy2: same as MATLAB
				for ( ii=0; ii<7; ii++){
					complex<double> fy2_add (fy2_temp[ii+8][0]/15.0, fy2_temp[ii+8][1]/15.0);
					fy2.push_back(fy2_add);
				}
				for ( ii=7; ii<15; ii++){ 
					complex<double> fy2_add (fy2_temp[ii-7][0]/15.0, fy2_temp[ii-7][1]/15.0);
					fy2.push_back(fy2_add);
				}
				//fftshift for fx2: same as MATLAB
				for ( ii=0; ii<45; ii++){
					complex<double> fx2_add (fx2_temp[ii+46][0]/91.0,fx2_temp[ii+46][1]/91.0);
					fx2.push_back(fx2_add);
				}
				for ( ii=45; ii<91; ii++){
					complex<double> fx2_add (fx2_temp[ii-45][0]/91.0,fx2_temp[ii-45][1]/91.0);
					fx2.push_back(fx2_add);
				}

				fx.push_back(fx1.size());
				fx.insert(fx.end(), fx1.begin(), fx1.end());
				fx.insert(fx.end(), fx2.begin(), fx2.end());
				fy.push_back(fy1.size());
				fy.insert(fy.end(), fy1.begin(), fy1.end());
				fy.insert(fy.end(), fy2.begin(), fy2.end());
			
				////////////////Nelder Mead non-linear fitting//////////////////
				////////////////////////////////////////////////////////////////

				////////////******* fit gx ********/////////////
				// Set all step sizes to 1 
				gsl_vector_set_all (ss, 1);
				gsl_vector_set (x, 0, 1.0);
				gsl_vector_set (x, 1, 0.0);
				minex_func.f = rss;
				minex_func.n = np;	
				minex_func.params = (void*)& (fx[0]);
				gsl_multimin_fminimizer_set (s, &minex_func, x, ss);
				int status;
				do{
					iter++;
					status = gsl_multimin_fminimizer_iterate(s); //perform a single iteration of the minimizer
					if (status)
					break;

					double size = gsl_multimin_fminimizer_size (s);
					status = gsl_multimin_test_size (size, 1e-8);
					/*
					if (status == GSL_SUCCESS){
						printf ("converged to minimum at\n");
					}

					printf ("%5d ", iter);
					for (ii = 0; ii < np; ii++){
						printf ("%10.16e ", gsl_vector_get (s->x, ii));
					}
					printf ("f() = %7.16f size = %.16f\n", s->fval, size);*/
				}
				while (status == GSL_CONTINUE && iter < 2000);
				iter = 0;
				a[i][j]  = gsl_vector_get(s->x,0);
				gx[i][j] = gsl_vector_get(s->x,1);
				gx[i][j] = -gx[i][j]*(fx1.size())*p/(lambda*L);

				//////////////******* fit gy *******////////////////
				gsl_vector_set_all (ss, 1);
				gsl_vector_set (x, 0, 1.0);
				gsl_vector_set (x, 1, 0.0);			
				minex_func.f = rss;
				minex_func.n = np;	
				minex_func.params = (void*)& (fy[0]);
				gsl_multimin_fminimizer_set (s, &minex_func, x, ss);
				do{
					iter++;
					status = gsl_multimin_fminimizer_iterate(s); //perform a single iteration of the minimizer

					if (status) 
					break;

					double size = gsl_multimin_fminimizer_size (s);
					status = gsl_multimin_test_size (size, 1e-8);
					/*
					if (status == GSL_SUCCESS){
						printf ("converged to minimum at\n");
					}

					printf ("%5d ", iter);
					for (ii = 0; ii < np; ii++){
						printf ("%10.16e ", gsl_vector_get (s->x, ii));
					}
					printf ("f() = %7.16f size = %.16f\n", s->fval, size);*/
				}
				while (status == GSL_CONTINUE && iter < 2000);
				iter = 0;
				gy[i][j] = gsl_vector_get(s->x,1);
				gy[i][j] = gy[i][j]*(fy1.size())*p/(lambda*L);

				aa = 0.0;
				fy.clear();
				fx.clear();
				fx2.clear();
				fy2.clear();
			}		
		}	
		cout<<i<<endl;
	}
/*
	FILE* fp;
    fp=fopen("/Users/admin/Documents/MATLAB/gx_gsl.txt","wt+");
    for(int i=0;i<121;i++){
        for(int j=0;j<121;j++)

           fprintf(fp,"%.10lf ", gx[i][j]);

        fprintf(fp, "\r\n");
    }
	fclose(fp);

	FILE* fp1;
    fp1=fopen("/Users/admin/Documents/MATLAB/gy_gsl.txt","wt+");
    for(int i=0;i<121;i++){
        for(int j=0;j<121;j++)

           fprintf(fp1,"%.10lf ", gy[i][j]);

        fprintf(fp1, "\r\n");
    }
	fclose(fp1);

	FILE* fp2;
    fp2=fopen("/Users/admin/Documents/MATLAB/a_gsl.txt","wt+");
    for(int i=0;i<121;i++){
        for(int j=0;j<121;j++)

           fprintf(fp2,"%.10lf ", a[i][j]);

        fprintf(fp2, "\r\n");
    }
	fclose(fp2);*/

	double w =1.0;

	/****************** FFT for gx and gy ********************/
	fftw_complex *in_gx;
	fftw_complex *in_gy;
	fftw_complex *out_gx_temp;
	fftw_complex *out_gy_temp;
	fftw_plan plan_fft_gx;
	fftw_plan plan_fft_gy;

	in_gx = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * row * column);
	in_gy = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * row * column);
	out_gx_temp = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * row * column);
	out_gy_temp = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * row * column);

	plan_fft_gx = fftw_plan_dft_2d(row, column, in_gx, out_gx_temp, FFTW_FORWARD, FFTW_ESTIMATE);
	plan_fft_gy = fftw_plan_dft_2d(row, column, in_gy, out_gy_temp, FFTW_FORWARD, FFTW_ESTIMATE);

	for (int i = 0; i < row; i++){
		for (int j = 0; j < column; j++){
			in_gx[i*column + j][0] = gx[i][j];
			in_gy[i*column + j][0] = gy[i][j];
			in_gx[i*column + j][1] = 0;
			in_gy[i*column + j][1] = 0;
		}
	}

	fftw_execute(plan_fft_gx);
	fftw_execute(plan_fft_gy);

	complex<double> tx_temp[row][column];
	complex<double> ty_temp[row][column];
	complex<double> tx[row][column];
	complex<double> ty[row][column];
	complex<double> c_temp[row][column];
	complex<double> c[row][column];
	complex<double> tmp;

	for (int i = 0; i < row; i++){
		for (int j = 0; j < column; j++){
			tx_temp[i][j] = complex<double>(out_gx_temp[i*column + j][0], out_gx_temp[i*column + j][1]);
			ty_temp[i][j] = complex<double>(out_gy_temp[i*column + j][0], out_gy_temp[i*column + j][1]);
		}
	}

	/******************** fftshift *****************correct*****/
	int global_temp = column;
	int midindex = ceil(global_temp/2.0);
	for (int i=0; i<midindex; i++){
		for (int j=0; j<midindex; j++){
			tx[i][j] = tx_temp[(i+midindex)%global_temp][(j+midindex)%global_temp];
			tx[global_temp-midindex+i][j] = tx_temp[i][(j+midindex)%global_temp];
			tx[i][global_temp-midindex+j] = tx_temp[(i+midindex)%global_temp][j];
			tx[global_temp-midindex+i][global_temp-midindex+j] = tx_temp[i][j];

			ty[i][j] = ty_temp[(i+midindex)%global_temp][(j+midindex)%global_temp];
			ty[global_temp-midindex+i][j] = ty_temp[i][(j+midindex)%global_temp];
			ty[i][global_temp-midindex+j] = ty_temp[(i+midindex)%global_temp][j];
			ty[global_temp-midindex+i][global_temp-midindex+j] = ty_temp[i][j];
		}
	}
	/*
	for (int i=0; i<midindex; i++){
		for (int j=0; j<midindex; j++){
			c[(i+midindex)%global_temp][(j+midindex)%global_temp] = tx[i][j];
			c[i][(j+midindex)%global_temp] = tx[global_temp-midindex+i][j];
			c[(i+midindex)%global_temp][j] = tx[i][global_temp-midindex+j];
			c[i][j] = tx[global_temp-midindex+i][global_temp-midindex+j];
		}
	}

	for (int i = 0; i<11; i++){
		for (int j=0; j<11; j++){
			cout<<c[i][j]<<" ";
		}
		cout<<endl;
	} */

	double kappax;
	double kappay;
	complex<double> im(0.0,1.0);
	for (int i=0; i<row; i++){
		for (int j=0; j<column; j++){
			kappax = 2*pi*(j+1-(floor(column/2.0)+1))/(column*dx);
			kappay = 2*pi*(i+1-(floor(row/2.0)+1))/(row*dy);
			if (kappax==0 && kappay==0)
				c_temp[i][j] = 0;
			else
				c_temp[i][j] = -im*(kappax*tx[i][j]+w*kappay*ty[i][j])/(kappax*kappax+w*kappay*kappay);
		}
	}
	/**************** ifftshift ******************/
	for (int i=0; i<midindex; i++){
		for (int j=0; j<midindex; j++){
			c[(i+midindex)%global_temp][(j+midindex)%global_temp] = c_temp[i][j];
			c[i][(j+midindex)%global_temp] = c_temp[global_temp-midindex+i][j];
			c[(i+midindex)%global_temp][j] = c_temp[i][global_temp-midindex+j];
			c[i][j] = c_temp[global_temp-midindex+i][global_temp-midindex+j];
		}
	}
    
	/*************** FFT for c ******************/
	fftw_complex *in_c;
	fftw_complex *out_phi_temp;
	fftw_plan plan_ifft_c;

	in_c = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * row * column);
	out_phi_temp = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * row * column);
	plan_ifft_c = fftw_plan_dft_2d(row, column, in_c, out_phi_temp, FFTW_BACKWARD, FFTW_ESTIMATE);

	for (int i = 0; i < row; i++){
		for (int j = 0; j < column; j++){
			in_c[i*column + j][0] = c[i][j].real();
			in_c[i*column + j][1] = c[i][j].imag();
		}
	}

	fftw_execute(plan_ifft_c);

	complex<double> phi[row][column];
	for (int i = 0; i < row; i++){
		for (int j = 0; j < column; j++){
			phi[i][j] = complex<double>(out_phi_temp[i*column + j][0]/(column*row), out_phi_temp[i*column + j][1]/(row*column));
		}
	}
/*
	FILE* fp3;
    fp3=fopen("/Users/admin/Documents/MATLAB/phi_gsl.txt","wt+");
    for(int i=0;i<row;i++){
        for(int j=0;j<column;j++)
           fprintf(fp3,"%.10lf ", phi[i][j].real());    
        fprintf(fp3,"\r\n");
    }
	fclose(fp3);*/

	finish_time = clock();
	runtime = double(finish_time-start_time)/CLOCKS_PER_SEC;
	cout<<runtime<<endl;
	//QueryPerformanceCounter(&cnt2); //get the final value of the timer
    //cout<<(double)(cnt2.QuadPart-cnt1.QuadPart)/(double)freq.QuadPart<<endl; //return the time (in seconds)
	
	cvNamedWindow("Image", CV_WINDOW_AUTOSIZE);
	cvShowImage("Image", LoadedImage);
	cvWaitKey(0);
	cvDestroyWindow("Image");
	cvReleaseImage(&LoadedImage);
	cvReleaseImage(&frame);
	cvReleaseImage(&temp);
	cvReleaseMat(&reference);

	gsl_multimin_fminimizer_free(s);
	gsl_vector_free(x);
	gsl_vector_free(ss);

	fftw_destroy_plan(plan_ifft_x1);
	fftw_destroy_plan(plan_ifft_y1);
	fftw_destroy_plan(plan_ifft_x2);
	fftw_destroy_plan(plan_ifft_y2);
	fftw_destroy_plan(plan_fft_gx);
	fftw_destroy_plan(plan_fft_gy);
	fftw_destroy_plan(plan_ifft_c);
    fftw_free(in_x1); 
	fftw_free(in_y1);
	fftw_free(in_x2); 
	fftw_free(in_y2);
	fftw_free(in_gx);
	fftw_free(in_gy); 
	fftw_free(in_c);
	fftw_free(fx1_temp);
	fftw_free(fy1_temp);
	fftw_free(fx2_temp);
	fftw_free(fy2_temp);
	fftw_free(out_gx_temp);
	fftw_free(out_gy_temp);
	fftw_free(out_phi_temp);

	return 0;
 }