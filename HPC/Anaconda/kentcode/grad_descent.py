# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 21:09:14 2014

@author: atif
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy import polyval, polyfit
from numpy import arange,array,ones,linalg
from pylab import plot,show
import argparse
import time

# m denotes the number of examples here, not the number of features
def gradientDescent(x, y, theta, alpha, m, numIterations):
    xTrans = x.transpose()
    for i in range(0, numIterations):
        hypothesis = np.dot(x, theta)
        loss = hypothesis - y
        # avg cost per example (the 2 in 2*m doesn't really matter here.
        # But to be consistent with the gradient, I include it)
        cost = np.sum(loss ** 2) / (2 * m)
#        print("Iteration %d | Cost: %f" % (i, cost))
        # avg gradient per example
        gradient = np.dot(xTrans, loss) / m
        # update
        theta = theta - alpha * gradient
    return theta


def genData(numPoints, bias, variance):
    x = np.zeros(shape=(numPoints, 2))
    y = np.zeros(shape=numPoints)
    # basically a straight line
    for i in range(0, numPoints):
        # bias feature
        x[i][0] = 1
        x[i][1] = i
        # our target variable
        y[i] = (i + bias) + random.uniform(0, 1) * variance
    return x, y

# gen 100 points with a bias of 25 and 10 variance as a bit of noise
start = time.clock()

x, y = genData(1000, 25, 10)
x1=x[:,1]
y1=y

#
print x1
print y1
#print len(x)
#print len(y)


elapsed =(time.clock()-start)

print 'Data gen time',elapsed


plt.plot(x1,y1,'ro')
plt.axis([0, 100, 0, 140])

#######################################################################################
#####################        poly fit command  ########################################
#######################################################################################

start = time.clock()


w = polyfit(x1,y1,1)
print ([w[1], w[0]])
t = np.arange(0., 100., 1)
plt.plot(t,w[1]+t*w[0])

elapsed =(time.clock()-start)

print 'Poly fit time',elapsed

#print timeit.Timer(stmt=test).timeit(number=100)

#(w,r_value,a1,b1,c1)=polyfit(x1,y,1,full=True)

#######################################################################################
#####################        gradient descent  ########################################
#######################################################################################

start = time.clock()

m, n = np.shape(x)
numIterations= 100000
alpha = .00005
theta = np.ones(n)
theta = gradientDescent(x, y, theta, alpha, m, numIterations)
print(theta)

plt.plot(t,theta[0]+t*theta[1])


elapsed =(time.clock()-start)

print 'Grad descent time',elapsed

#######################################################################################
#####################        leastsquare       ########################################
#######################################################################################

#def func(x, a, b):
#    return a + b*x
#x0    = numpy.array([0.0, 0.0])
#import scipy.optimize as optimization
#
#print optimization.curve_fit(func, x1, y1, x0)