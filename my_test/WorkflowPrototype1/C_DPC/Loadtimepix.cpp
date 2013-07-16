#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

IplImage* Loadtimepix( IplImage* InputImage )
 {
	CvMat* datax = cvCreateMat( 516, 512, CV_64FC1 );
	CvMat* datay = cvCreateMat( 516, 516, CV_64FC1 );
	CvMat* data  = cvCreateMat( 516, 516, CV_64FC1 );
	cvZero( data );

	CvMat* data0 = cvCreateMat( 512, 512, CV_64FC1 );
    cvConvert ( InputImage, data0 );

	int step = data0->step/sizeof( double );  // step is the number of cols
		
	double *data0_ptr = data0->data.db;
	double *datax_ptr = datax->data.db;
	double *datay_ptr = datay->data.db;

	/*** convert row from 512 to 516 ***/
	for ( int i = 0; i<=254; i++ )
	{
		for ( int j = 0; j<=511; j++ )
		{
			( datax_ptr + i*step )[j] = ( data0_ptr+i*step )[j];
		}
	}
	for ( int i = 0; i<=2; i++ )
	{
		for ( int j = 0; j<=511; j++ )
		{
			( datax_ptr+( i+255 )*step )[j] = ( data0_ptr+255*step )[j]/3;
		}
	}
	for ( int i = 0; i<=2; i++ )
	{
		for ( int j = 0; j<=511; j++ )
		{
			( datax_ptr+( i+258 )*step )[j] = ( data0_ptr+256*step )[j]/3;
		}
	}
	for ( int i = 0; i<=254; i++ )
	{
		for ( int j = 0; j<=511; j++ )
		{
			( datax_ptr+( i+261 )*step )[j] = ( data0_ptr + ( 257 + i ) * step )[j];
		}
	}

	/*** convert columns from 512 to 516 ***/
    for (int j = 0; j<=254; j++)
	{
		for (int i = 0; i<=515; i++)
		{
			(datay_ptr+i*516)[j] = (datax_ptr+i*step)[j];
		}
	}
	for (int j = 0; j<=2; j++)
	{
		for (int i = 0; i<=515; i++)
		{
			(datay_ptr+i*516)[j+255] = (datax_ptr+i*step)[255]/3;
		}
	}
	for (int j = 0; j<=2; j++)
	{
		for (int i = 0; i<=515; i++)
		{
			(datay_ptr+i*516)[j+258] = (datax_ptr+i*step)[256]/3;
		}
	}
	for (int j = 0; j<=254; j++)
	{
		for (int i = 0; i<=515; i++)
		{
			(datay_ptr+i*516)[j+261] = (datax_ptr+i*step)[j+257];
		}
	}

	cvAdd(datay, data, data);   // assume references = 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	IplImage* pImg = NULL;
	pImg = cvCreateImage(cvSize(516, 516), IPL_DEPTH_64F, 1);
    cvConvert(data, pImg); 
    
	return pImg;

	cvReleaseMat( &data );
	cvReleaseMat( &datax );
	cvReleaseMat( &datay );
	cvReleaseMat( &data0 );
	cvReleaseImage ( &pImg );
 }