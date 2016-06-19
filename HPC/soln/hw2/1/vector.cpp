#include <math.h>
#include <iostream>
#include <sys/time.h>
#include <fstream>
using namespace std;

extern "C"{
double ddot_( const int *N, const double *a, const int *inca, const double *b, const int *incb );
}

double ddot( int N, double *a, int inca, double *b, int incb ){
  return ddot_( &N, a, &inca, b, &incb );
}

int main( int argc, char** argv ){
  struct timeval t0, t1 ;
  int m,irep,i;
  double nrep, dt,flops;
  ofstream out_data("lblas.txt");
  for (m=1;m<1000000000;m*=10)
  {
    nrep = (pow(10,9))/(2*m+1);
  double *a=  new double[m];
  double *b= new double[m];
   for (i=1;i<m;i++)
	{
	  a[i] =i+1;
	  b[i] = i+3;
	}
   gettimeofday(&t0,NULL);
  for (irep=1;irep<nrep;irep++){
  double dot_product = ddot( m, a, 1, b, 1 );
  }
  gettimeofday(&t1,NULL);
  long elapsed = (t1.tv_sec-t0.tv_sec)*1000000 + t1.tv_usec-t0.tv_usec;
  dt=elapsed/((float) 1000000);
  dt=dt/((float) nrep); 
  flops =(2*m+1)/dt;
  out_data<<flops/1000000<<"  "<<m<<endl;
  cout<<flops/1000000<<"  "<<m<<"  "<<dt<<endl;
   }
  
  return 0;}
