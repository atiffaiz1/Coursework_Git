#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <math.h>


int main(int argc, char** argv)
{
  int nrep,irep,i;
  double m,*a,*b,dot_pdt;
  struct timeval t0,t1;

 for(m=1;m<100000;m*10){
   nrep=(10^7)/(2*m+1);
   /*a=malloc(m*sizeof(double));
     b=malloc(m*sizeof(double));*/
   a=malloc(sizeof(double)*(m));
   b=malloc(sizeof(double)*m);
   for(i=1;i<m;i++){
     a[i]=i+1;
     b[i]=i+2;
   }
   gettimeofday(&t0,NULL);
   for(irep=1;irep<nrep;irep++){
     dot_pdt=ddot_(m,a,1,b,1);
   }
 }
 
 gettimeofday(&t1,NULL);

 long elapsed = (t1.tv_sec-t0.tv_sec)*1000000 + t1.tv_usec-t0.tv_usec;
 double dt=elapsed/((float)1000000);
 dt=dt/((float)nrep);
 
   double flops=(2*m+1)/dt;
   printf("%d\n",flops);
   printf("%i\n",m);
   return 0;
 }
/*
start=clock();
 int m[10000000];
 int n[10000000];

  int i,j;


 double result;
 /*if(ptr==NULL){
	printf("Error");
	exit(0);
	}*/

  /*  for(i=0;i<10;i++)
    scanf("%lf",&m[i]);
  for(i=0;i<10;i++)
  scanf("%lf",&n[i]); 
  for(i=0;i<10000000;i++){
    m[i]=i;
 /* printf("%d",m[i]);
  printf("\n");
  }
  for(j=0;j<10000000;j++){
    n[j]=j*j;
    /*printf("%d",n[j]);
    printf("\n");
    }
 
 /* double result=(float)malloc(sizeof(double));
   result=ddot_(5,m,1,n,1);
   printf("%d\n",result); 
  
end=clock();
cpu_time_used =((int)(end-start))/ CLOCKS_PER_SEC;
/*printf("%d\n",cpu_time_used);
  return 0;
}
*/
