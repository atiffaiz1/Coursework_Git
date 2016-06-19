from numpy import arange,array,ones,linalg
from pylab import plot,show

xi = arange(0,9)
#A = array([ xi, ones(9)])
#print A
#print A.T
# linearly generated sequence
y = [19, 20, 20.5, 21.5, 22, 23, 23, 25.5, 24]
(w,r,a,b,c) = polyfit(xi,y,1,full=True) # obtaining the parameters
print w
print r
# plotting the line
line = w[0]*xi+w[1] # regression line
plot(xi,line,'r-',xi,y,'o')
show()