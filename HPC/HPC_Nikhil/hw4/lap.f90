program lap
Use omp_lib
implicit none

double precision :: dx,dy,dt, pi=3.14, norm, t_start,t_end
integer :: Nx,Ny,i,j,n,Nt,nitr, Np, Nperprocess
double precision, dimension(2000) ::x,y
double precision, dimension(2000,2000) :: phi,phio
integer, dimension(8) :: Nthreads
Nthreads=(/ 1, 2, 3, 4, 5, 6, 7, 8/)
do i=1,100
   do j=1,100
      phio(i,j)=1.0
   end do
end do
open(1,file='result.txt')
n=1000000
dt=0.01
Nt=int(n/dt)
dx=0.01
dy=0.01
Nx=2000
Ny=2000

do ntr=1,size(Nthreads)
call OMP_SET_NUM_THREADS(Nt)
!$OMP PARALLEL DO
 myid = OMP_GET_THREAD_NUM()
 Nt = omp_get_num_threads()
 Np=omp_get_num_procs()
 Nperprocess= N/Nt
  t_start = OMP_GET_WTIME()


do i=1,Nx
   x(i)=i*dx
   y(i)=i*dy
   !print *,x(i)
end do

timeloop: do nitr=1,Nt
   
   do i=1,2000
      phio(1,i)=sin(pi*x(i))
      phio(Nx,i)=sin(pi*x(i))*exp(-pi)
      phio(:,1)=0.0
      phio(:,Ny)=0.0
   end do

   do i=2,Nx-1
      do j=2,Ny-1
         phi(i,j)=(phio(i+1,j)+phio(i,j+1)+phio(i-1,j)+phio(i,j-1))/4
 
         !print *,norm
         IF (abs(phio(i,j)-phi(i,j))<(10**-5)) exit timeloop
      end do
   end do
  
   phio=phi
end do timeloop
do i=1,Nx
   do j=1,Ny
      !write(1,*) phi(i,j)
      !print *,phi(i,j)
   end do
   !write(1,*)phi(i,:)
   !write(1,*)''
end do
 t_end = OMP_GET_WTIME()
 tot_time = t_end - t_start

end do
close(1)
!print *,nitr
end program
