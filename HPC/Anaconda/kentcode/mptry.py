#!/bin/env python
import sys
import random
import time
import multiprocessing
import numpy as np


start = time.clock()


numitems = 1000
nprocs = 4
sum=0.0


def partition(lst, n):
  division = len(lst) / float(n)
  
  p = [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n) ]
  #print 'p=', p
  return p


def myRunningSum(l):
    global sum
    #sum = np.zeros(numpows)
    # print 'sum',sum
    s=l[0]+1
    e=l[(len(l)-1)]+1
    #print 'l',e
    
    for j in xrange(s,e,2):
        
        
        sum= sum + 1.0/(2*j-1)- 1.0/(2*j+1)
        #print 'sum',sum

    
    #print 'sum',sum
    time.sleep(5)    
    return sum



if __name__ == '__main__':

  random.seed(1)
  data = range(numitems)
#  print data
  pool = multiprocessing.Pool(processes=nprocs,)
  calculations = pool.map(myRunningSum, partition(data,nprocs))

#  print 'Answer is:', listsum(calculations)
  pi= calculations[0]*4
  print 'Answer is:', pi
  sum=sum*4
  print 'globalsum',sum
  elapsed =(time.clock()-start)

  print 'Data gen time',elapsed
