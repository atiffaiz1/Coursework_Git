program PIomp
Use omp_lib
implicit none

double precision   :: mysum,pi
double precision   :: t_start, t_end, tot_time
integer            :: Mflops, myid,Np,Nt, Nperprocess
integer            ::i,j,k,N, ntr
integer, dimension(1) :: Ninput
integer, dimension(8) :: Nthreads
open(1, file='result_1000000.txt')

Ninput =(/1000000 /)
Nthreads=(/ 1, 2, 3, 4, 5, 6, 7, 8/)
do ntr=1,size(Nthreads)
Nt=Nthreads(ntr)
!print *, Nt
call OMP_SET_NUM_THREADS(Nt)
!$OMP PARALLEL DO
do i=1,size(Ninput)
  N=Ninput(i)
 mysum =0.0



 myid = OMP_GET_THREAD_NUM()
 Nt = omp_get_num_threads()
 Np=omp_get_num_procs()
 Nperprocess= N/Nt
  t_start = OMP_GET_WTIME()
!print *, N, Np, Nt, myid, Nperprocess
 do j = 1,1000

   do k=myid*(N/Nt)+1,(myid+1)*(N/Nt),2
     
    mysum = mysum + 1.0/real(2*k-1)
    mysum = mysum - 1.0/real(2*k+1)

   end do

 end do

 pi = mysum*4/1000
 

 t_end = OMP_GET_WTIME()
 tot_time = t_end - t_start

 Mflops = int(real((N*10)*1000)/(1000000*tot_time))

print *, N, Nt, tot_time
write(1,*)N, Nt, tot_time

end do
!$OMP END PARALLEL DO
end do

end program
 
