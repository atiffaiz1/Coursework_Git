# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 12:25:02 2014

@author: atif
"""

# -*- coding: utf-8 -*-

# do Linear Regression with Argparse
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from scipy import polyval, polyfit
from numpy import arange,array,ones,linalg
from pylab import plot,show
import argparse


#######################################################################
#this function is used to test the dump file's contents to make sure their actual
#data and not blank or invalid formats
def is_number(s):
    try:
        float(s)
        return s
    except ValueError:
        return 0
 


#Used to extend the linear regression and compound plot lines so that they go past
#the max and min of their data sets
def extended(ax, x, y, **args):

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    x_ext = np.linspace(xlim[0], xlim[1], 100)
    p = np.polyfit(x, y , deg=1)
    y_ext = np.poly1d(p)(x_ext)
    ax.plot(x_ext, y_ext, **args)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return ax
    
## Save LR data into file
def write(m,b,r_squared,property,x,y):
    mm = str(m)
    bb = str(b)
    rr = str(r_squared)
    txt = open('projectionvalues.txt', 'a')
    txt.write(property),txt.write("_"),txt.write(x),txt.write("_"),
    txt.write(y),txt.write("                    "),txt.write(mm),txt.write("     "),
    txt.write(bb),txt.write("     "),txt.write(rr),txt.write("\n")
    txt.close()
    
def write_outlier(m,b,r_squared,property,x,y,percentage):
    mm = str(m)
    bb = str(b)
    rr = str(r_squared)
    txt = open('projectionvalues.txt', 'a')
    txt.write(property),txt.write("_"),txt.write(x),txt.write("_"),
    txt.write(y),txt.write("_outlier_"),txt.write(percentage),txt.write("%"),
    txt.write("      "),txt.write(mm),txt.write("     "),
    txt.write(bb),txt.write("     "),txt.write(rr),txt.write("\n")
    txt.close()

def write_remained(m,b,r_squared,property,x,y,percentage):
    mm = str(m)
    bb = str(b)
    rr = str(r_squared)
    txt = open('projectionvalues.txt', 'a')
    txt.write(property),txt.write("_"),txt.write(x),txt.write("_"),
    txt.write(y),txt.write("_remained_"),txt.write(percentage),txt.write("%"),
    txt.write("     "),txt.write(mm),txt.write("     "),
    txt.write(bb),txt.write("     "),txt.write(rr),txt.write("\n")
    txt.close()
############################################################################### 
### the HelpFormatter and provide a special intro for the options that should be handled "raw"
### Any other calls to .add_argument() where the help does not start with R| will be wrapped as normal.
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()  
        return argparse.HelpFormatter._split_lines(self, text, width)
        

       
parser = argparse.ArgumentParser(description="Do Linear Regression to the data", 
                                 formatter_class=SmartFormatter)
                           
                                 
parser.add_argument("infile", type=str, help="input the name of data file")    
                            
parser.add_argument("property", type=int, choices=[1,2,3,4],
                    help="R|choose the options of property:\n"
                    "1 = HOMO  2 = LUMO  3 = Dipole  4 = Gap")
                    
parser.add_argument("percent_outlier", type=float, help="R|define the outlier\n"
                    "enter the percentage of data taken out to be outliers\n"
                    "input only number part")
                    
parser.add_argument("-x", "--x_flavor", type=int, 
                    choices=[1,2], help="R|choose the flavor for x-axis:\n"
                    "1 = BP86/SVP    2 = B3LYP/SVP")
                    
parser.add_argument("-y", "--y_flavor", type=int, 
                    choices=[1,2,3,4,5,6,7,8,9], help="R|choose the flavor for y-axis:\n"
                    "1 = BP86/SVP    2 = B3LYP/SVP  3 = PBE0/SVP \n4 = BH&HLYP/SVP 5 = M06-2X/SVP"
                    " 6 = HF/SVP \n7 = BP86/TZVP   8 = B3LYP/TZVP 9 = PBE0/TZVP")

parser.add_argument("-rb","--result_box",action='store_false',default=True,
                    help="Hide the result display box in all plots")
                    
parser.add_argument("-rb1","--result_box1",action='store_false',default=True,
                    help="Hide the result display box only in original data pool")
                    
parser.add_argument("-rb2","--result_box2",action='store_false',default=True,
                    help="Hide the result display box only in outlier")
                    
parser.add_argument("-rb3","--result_box3",action='store_false',default=True,
                    help="Hide the result display box only in remaining pool")
                    
parser.add_argument("-lr","--lr_line",action='store_false',default=True,
                    help="Hide all the LinearReg lines.")
                    
parser.add_argument("-lr1","--lr_line1",action='store_false',default=True,
                    help="Hide the LinearReg line for original data pool.")
                    
parser.add_argument("-lr2","--lr_line2",action='store_false',default=True,
                    help="Hide the LinearReg line for outliers.")
                    
parser.add_argument("-lr3","--lr_line3",action='store_false',default=True,
                    help="Hide the LinearReg line for remaining pool.")

parser.add_argument("-his","--histogram",action='store_false',default=True,
                    help="Do not generate historgram of the projection discrepancy")
                    
args = parser.parse_args('testlr.dat 1 5 -x 1 -y 4 -lr2 -lr3'.split())
#args = parser.parse_args()

###percent_outlier
num_percentage = str(args.percent_outlier)

### property
if args.property == 1:
    pro_name = "HOMO"
    line_color = "Blue"
    num1 = -9.00  #for ax.set_xlim and ax.set_ylim
    num2 = -3.00  #for ax.set_xlim and ax.set_ylim
elif args.property == 2:
    pro_name = "LUMO"
    line_color = "Red"
    num1 = -6.00 #for ax.set_xlim and ax.set_ylim
    num2 = 3.00  #for ax.set_xlim and ax.set_ylim
elif args.property == 3:
    pro_name = "Dipole"
    line_color = "Violet"
    num1 = -1.00  #for ax.set_xlim and ax.set_ylim
    num2 = 14.00  #for ax.set_xlim and ax.set_ylim
elif args.property == 4:
    pro_name = "Gap"
    line_color = "Green"
    num1 = 0.00  #for ax.set_xlim and ax.set_ylim
    num2 = 10.00  #for ax.set_xlim and ax.set_ylim

### x-flavor, y-flavor
if args.x_flavor == 1:
    x_name = "BP86s"
    x_fname = "BP86/SVP"
    #Used to get rid of obvious outliers that have been brought into the data 
    if args.property == 1: #HOMO
    
        if args.y_flavor != 6: # for all y flavors except HF  #HOMO,BP86s
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.24) and i[0]<=(-0.12):
                    if i[1]>=(-0.30) and i[1]<=(-0.14):
                        return True
                else:
                    return False
        else: # only for HF (y flavor) #HOMO,BP86s
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.24) and i[0]<=(-0.12):
                    if i[1]>=(-0.60) and i[1]<=(-0.14):
                        return True
                else:
                    return False
    ####                
    elif args.property == 2: #LUMO,BP86s
    
        if args.y_flavor != 6: # for all y flavors except HF  #LUMO,BP86s
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.20) and i[0]<=(0.0):
                    if i[1]>=(-0.20) and i[1]<=(0.05):
                        return True
                else:
                    return False
        else: # only for HF (y flavor) #LUMO,BP86s
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.20) and i[0]<=(0.10):
                    if i[1]>=(-0.20) and i[1]<=(0.30):
                        return True
                else:
                    return False
    ###
    elif args.property == 3: #Dipole,BP86s
    
        if args.y_flavor != 6: # for all y flavors except HF  #Dipole,BP86s
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.10) and i[0]<=(13.0):
                    if i[1]>=(-0.10) and i[1]<=(13.0):
                        return True
                else:
                    return False
        else: # only for HF (y flavor) #Dipole,BP86s
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.10) and i[0]<=(13.0):
                    if i[1]>=(-0.10) and i[1]<=(13.0):
                        return True
                else:
                    return False
                    
    ###
    elif args.property == 4: #Gap,BP86s
    
        def lrboundaries(s,t):
            #i[0] is x, i[1] is y, first term is min, second is max
            if i[0]>=(0.0) and i[0]<=(0.15):
                if i[1]>=(0.0) and i[1]<=(0.40):
                    return True
            else:
                return False

        
            
        
        
elif  args.x_flavor == 2:
    x_name = "B3LYPs"
    x_fname = "B3LYP/SVP"
    #Used to get rid of obvious outliers that have been brought into the data
    if args.property == 1: #HOMO,B3LYPs
    
        if args.y_flavor != 6: # for all y flavors except HF #HOMO
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.28) and i[0]<=(-0.14):
                    if i[1]>=(-0.30) and i[1]<=(-0.14):
                        return True
                else:
                    return False
        else: # only for HF (y flavor) #HOMO
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.24) and i[0]<=(-0.12):
                    if i[1]>=(-0.60) and i[1]<=(-0.14):
                        return True
                else:
                    return False
    ###
    elif args.property == 2: #LUMO,B3LYPs
    
        if args.y_flavor != 6: # for all y flavors except HF  #LUMO,B3LYPs
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.20) and i[0]<=(0.05):
                    if i[1]>=(-0.20) and i[1]<=(0.05):
                        return True
                else:
                    return False
        else: # only for HF (y flavor) #LUMO,B3LYPs
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.20) and i[0]<=(0.10):
                    if i[1]>=(-0.20) and i[1]<=(0.30):
                        return True
                else:
                    return False
    ###
    elif args.property == 3: #Dipole,B3LYPs
    
        if args.y_flavor != 6: # for all y flavors except HF  #Dipole,B3LYPs
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.10) and i[0]<=(13.0):
                    if i[1]>=(-0.10) and i[1]<=(13.0):
                        return True
                else:
                    return False
        else: # only for HF (y flavor) #Dipole,B3LYPs
            def lrboundaries(s,t):
                #i[0] is x, i[1] is y, first term is min, second is max
                if i[0]>=(-0.10) and i[0]<=(13.0):
                    if i[1]>=(-0.10) and i[1]<=(13.0):
                        return True
                else:
                    return False
    ###
    elif args.property == 4: #Gap,B3LYPs
    
        def lrboundaries(s,t):
            #i[0] is x, i[1] is y, first term is min, second is max
            if i[0]>=(0.0) and i[0]<=(0.20):
                if i[1]>=(0.0) and i[1]<=(0.40):
                    return True
            else:
                return False

elif  args.x_flavor == 3:
    x_name = "PBE0s"
elif  args.x_flavor == 4:
    x_name = "BHHLYPs"
elif  args.x_flavor == 5:
    x_name = "M06s"
elif  args.x_flavor == 6:
    x_name = "HFs"
elif  args.x_flavor == 7:
    x_name = "BP86t"
elif  args.x_flavor == 8:
    x_name = "B3LYPt"
elif  args.x_flavor == 9:
    x_name = "PBE0t"
    
if args.y_flavor == 1:
    y_name = "BP86s"
    y_fname = "BP86/SVP"
elif  args.y_flavor == 2:
    y_name = "B3LYPs"
    y_fname = "B3LYP/SVP"
elif  args.y_flavor == 3:
    y_name = "PBE0s"
    y_fname = "PBE0/SVP"
elif  args.y_flavor == 4:
    y_name = "BHHLYPs"
    y_fname = "BH&HLYP/SVP"
elif  args.y_flavor == 5:
    y_name = "M06s"
    y_fname = "M06/SVP"
elif  args.y_flavor == 6:
    y_name = "HFs"
    y_fname = "HF/SVP"
elif  args.y_flavor == 7:
    y_name = "BP86t"
    y_fname = "BP86/TZVP"
elif  args.y_flavor == 8:
    y_name = "B3LYPt"
    y_fname = "B3LYP/TZVP"
elif  args.y_flavor == 9:
    y_name = "PBE0t"
    y_fname = "PBE0/TZVP"


lr_plot = "lr_%s_%s_%s.png" % (pro_name, x_name, y_name)
lr_histogram = "Hist_%s_%s_%s.png" % (pro_name, x_name, y_name)
num5 = str(int(args.percent_outlier * 100))
lr_plot_outlier = "lr_%s_%s_%s_outlier_%s.png" % (pro_name, x_name, y_name, num5)
lr_plot_remained = "lr_%s_%s_%s_remained_%s.png" % (pro_name, x_name, y_name, num5)
lr_text_outlier = "lr_%s_%s_%s_outlier_%s" % (pro_name, x_name, y_name, num5)
projection_discrepancy = "discrepancy_%s_%s_%s"% (pro_name, x_name, y_name)



#used to count the amount of lines in my file, -2 is for the lines that dont't matter, the heading
num_lines = sum(1 for line in open(args.infile))
x_array = np.zeros(num_lines-2)
y_array = np.zeros(num_lines-2)



with open(args.infile) as f:
    for _ in xrange(2):
        next(f)
    for i,line in enumerate(f):
        values = line.strip().split(',')
        x_array[i] = is_number((values[args.x_flavor + 1]))
        y_array[i] = is_number((values[args.y_flavor + 1]))
f.close()
##########################################################################


z = zip(x_array,y_array)
x1=[]
y1=[]
for i in z:
    if i[0] and i[1]!=0:
        #line[0] is x and line[1] is y
        if lrboundaries(i[0],i[1])==True:  
            if args.property == 3:  #only for Dipole
                x1.append(i[0])
                y1.append(i[1])
            else:
                x1.append(i[0]*27.21139570)
                y1.append(i[1]*27.21139570)
b1=x1
#linear regression using stats.linregress
#slope, intercept, r_value, p_value, std_err = stats.linregress(x1,y1)
#
#
#this will find your y-intercept and slope of your linear regression line and 
#then will create points where a line is plotted on
(w,r_value,a1,b1,c1)=polyfit(x1,y1,1,full=True)
m=w[0]
b=w[1]
r_squared= r_value**2
yp=polyval(w,x1)
yp1=yp
stand = (np.std(x1) + np.std(y1))/2
print 'r-squared: ', r_squared
print 'stand: ', stand

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['mathtext.default'] = 'regular'
fig= plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.scatter(x1,y1,s=0.5,color='Black')


textstr = '$R^2:\ \ \ \ \ \ \  %.4f$\n$slope:\ \ \ %.4f$\n$shift:\ \ \ \ \ %.4f$'%(r_squared, m, b)
props = dict(boxstyle='round', facecolor= 'White', alpha=1.0)

if args.result_box == True and args.result_box1 == True:
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
        
write(m,b,r_squared,pro_name,x_name,y_name)

if args.property == 1:
    ax.set_xlabel(r'$\epsilon\ $HOMO (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\epsilon\ $HOMO (%s) [eV]'%(y_fname), fontsize='x-large')
elif args.property == 2:
    ax.set_xlabel(r'$\epsilon\ $LUMO (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\epsilon\ $LUMO (%s) [eV]'%(y_fname), fontsize='x-large')
elif args.property == 3:
    ax.set_xlabel(r'$\mu\ $  (%s) [D]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\mu\ $  (%s) [D]'%(y_fname), fontsize='x-large')
elif args.property == 4:
    ax.set_xlabel(r'$\Delta\ \epsilon\ $  (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\Delta\ \epsilon\ $  (%s) [eV]'%(y_fname), fontsize='x-large')

ax.tick_params(labelsize='large')
ax.set_xlim((num1),(num2))
ax.set_ylim((num1),(num2))

if args.lr_line == True and args.lr_line1 == True:
    ax = extended(ax, x1, yp, lw=2.4, color = line_color)
#ax.plot(x1,yp,'green',linewidth=1.0)
ax.grid(True)

plt.savefig(lr_plot)
#plt.show(ax)

##########################################################################


# save outliers into a list 
def_outlier = args.percent_outlier * 0.01 #define what percentage of datas are taken out  
dis = []
dis_raw = []
# turn list x1 and y1 into array
z2 = zip(x1,y1)
x_and_y = np.asarray(z2)


#def predicted_y(x):
#    predicted_y_value = slope * x + intercept
#    return predicted_y_value

# calculte the distance from each point to regression line 
for (x,y) in x_and_y:
    distance = m*x+b - y
    
    dis_raw = np.append(dis_raw,[distance])

dis = np.absolute(dis_raw)

##save discrepancy into a python array file
#np.save(projection_discrepancy, dis_raw)


    
# get an array (x,y,distance) and make it sorted by order of distance (low to high)
x_y_dis= np.concatenate((x_and_y,dis[:,np.newaxis]), axis=1)
x_y_dis_sorted = x_y_dis[x_y_dis[:,2].argsort()]

# extract the outliers of specified percentage from the data 
num3 = len(x_y_dis_sorted) - int(len(x_y_dis_sorted) * def_outlier)
x_y_dis_remained = x_y_dis_sorted[0:num3, :]
x_y_dis_outlier = x_y_dis_sorted[num3:len(x_y_dis_sorted), :]

##save outlier into file
#if args.property == 3:  #only for Dipole
#    np.save(lr_text_outlier, x_y_dis_outlier)
#else:
#    array1 = np.array([27.21139570,27.21139570,1], float)
#    x_y_dis_outlier2 =  x_y_dis_outlier / array1
#    np.save(lr_text_outlier, x_y_dis_outlier2)


x_xydisoutlier = x_y_dis_outlier[:,0].tolist()
y_xydisoutlier = x_y_dis_outlier[:,1].tolist()
x_xydisremained = x_y_dis_remained[:,0].tolist()
y_xydisremained = x_y_dis_remained[:,1].tolist()
    
###linear regression for outliers
#slope, intercept, r_value, p_value, std_err = stats.linregress(x_xydisoutlier,y_xydisoutlier)
#
#
#this will find your y-intercept and slope of your linear regression line and 
#then will create points where a line is plotted on
(w2,r_value,a2,b2,c2)=polyfit(x_xydisoutlier,y_xydisoutlier,1,full=True)
m2=w2[0]
b2=w2[1]
r_squared= r_value**2
yp2=polyval(w2,x_xydisoutlier)
yp1=yp2
stand = (np.std(x_xydisoutlier) + np.std(y_xydisoutlier))/2
#print 'r-squared: ', r_squared
print 'stand: ', stand

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['mathtext.default'] = 'regular'
fig= plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.scatter(x_xydisoutlier,y_xydisoutlier,s=0.5,color='Black')


textstr = '<Outliers>\n$R^2:\ \ \ \ \ \ \  %.4f$\n$slope:\ \ \ %.4f$\n$shift:\ \ \ \ \ %.4f$'%(r_squared, m2, b2)
props = dict(boxstyle='round', facecolor= 'White', alpha=1.0)

if args.result_box == True and args.result_box2 == True:
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
        
write_outlier(m2,b2,r_squared,pro_name,x_name,y_name,num_percentage)

if args.property == 1:
    ax.set_xlabel(r'$\epsilon\ $HOMO (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\epsilon\ $HOMO (%s) [eV]'%(y_fname), fontsize='x-large')
elif args.property == 2:
    ax.set_xlabel(r'$\epsilon\ $LUMO (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\epsilon\ $LUMO (%s) [eV]'%(y_fname), fontsize='x-large')
elif args.property == 3:
    ax.set_xlabel(r'$\mu\ $  (%s) [D]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\mu\ $  (%s) [D]'%(y_fname), fontsize='x-large')
elif args.property == 4:
    ax.set_xlabel(r'$\Delta\ \epsilon\ $  (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\Delta\ \epsilon\ $  (%s) [eV]'%(y_fname), fontsize='x-large')

ax.tick_params(labelsize='large')
ax.set_xlim((num1),(num2))
ax.set_ylim((num1),(num2))

if args.lr_line == True and args.lr_line2 == True:
    ax = extended(ax, x_xydisoutlier, yp2, lw=2.4, color = line_color)
#ax.plot(x1,yp,'green',linewidth=1.0)
ax.grid(True)

plt.savefig(lr_plot_outlier)
#plt.show(ax)


#########################################################################


###linear regression for the remained
#slope, intercept, r_value, p_value, std_err = stats.linregress(x_xydisremained,y_xydisremained)

#
#this will find your y-intercept and slope of your linear regression line and 
#then will create points where a line is plotted on

(w3,r_value,a3,b3,c3)=polyfit(x_xydisremained,y_xydisremained,1,full=True)
yp2=polyval(w3,x_xydisremained)
m3=w3[0]
b3=w3[1]
r_squared= r_value**2
yp1=yp2
stand = (np.std(x_xydisremained) + np.std(y_xydisremained))/2
print 'r-squared: ', r_squared
print 'stand: ', stand

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['mathtext.default'] = 'regular'
fig= plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.scatter(x_xydisremained,y_xydisremained,s=0.5,color='Black')


textstr = '<Remained>\n$R^2:\ \ \ \ \ \ \  %.4f$\n$slope:\ \ \ %.4f$\n$shift:\ \ \ \ \ %.4f$'%(r_squared, m3, b3)
props = dict(boxstyle='round', facecolor= 'White', alpha=1.0)

if args.result_box == True and args.result_box3 == True:
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
        
write_remained(m3,b3,r_squared,pro_name,x_name,y_name,num_percentage)

if args.property == 1:
    ax.set_xlabel(r'$\epsilon\ $HOMO (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\epsilon\ $HOMO (%s) [eV]'%(y_fname), fontsize='x-large')
elif args.property == 2:
    ax.set_xlabel(r'$\epsilon\ $LUMO (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\epsilon\ $LUMO (%s) [eV]'%(y_fname), fontsize='x-large')
elif args.property == 3:
    ax.set_xlabel(r'$\mu\ $  (%s) [D]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\mu\ $  (%s) [D]'%(y_fname), fontsize='x-large')
elif args.property == 4:
    ax.set_xlabel(r'$\Delta\ \epsilon\ $  (%s) [eV]'%(x_fname), fontsize='x-large')
    ax.set_ylabel(r'$\Delta\ \epsilon\ $  (%s) [eV]'%(y_fname), fontsize='x-large')

ax.tick_params(labelsize='large')
ax.set_xlim((num1),(num2))
ax.set_ylim((num1),(num2))

if args.lr_line == True and args.lr_line3 == True:
    ax = extended(ax, x_xydisremained, yp2, lw=2.4, color = line_color)
#ax.plot(x1,yp,'green',linewidth=1.0)
ax.grid(True)

plt.savefig(lr_plot_remained)
#plt.show(ax)
#########################################################################
# Create a histogram for the projection discrepancy
if args.histogram == True:
    fig= plt.figure()
    ax = fig.add_subplot(111)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['mathtext.default'] = 'regular'
    ax.tick_params(labelsize='large')
    ax.grid(True)
    if args.property == 1:
        ax.set_xlabel("$\epsilon\ $ $\Delta$%s Values [eV]" %(pro_name), fontsize='x-large')
    elif args.property == 2:
        ax.set_xlabel("$\epsilon\ $ $\Delta$%s Values [eV]" %(pro_name), fontsize='x-large')       
    elif args.property == 3:
        ax.set_xlabel(r'$\mu\ $%s Values [D]' %(pro_name), fontsize='x-large')
    elif args.property == 4:
        ax.set_xlabel("$\Delta\ \epsilon\ $%s Values [eV]" %(pro_name), fontsize='x-large')       
    ax.set_ylabel('Frequency', fontsize='x-large')
    plt.yscale('log', nonposy='clip')
    props = dict(boxstyle='round', facecolor= 'White', alpha=1.0)
    if args.property == 1:
        textstr= "$\epsilon\ $%s \n  (%s) [eV] \n vs. \n (%s) [eV]" %(pro_name,x_fname,y_fname)
    elif args.property == 2:
        textstr= "$\epsilon\ $%s \n  (%s) [eV] \n vs. \n (%s) [eV]" %(pro_name,x_fname,y_fname)       
    elif args.property == 3:
        textstr= "$\mu\ $%s \n  (%s) [eV] \n vs. \n (%s) [eV]" %(pro_name,x_fname,y_fname)        
    elif args.property == 4:
        textstr= "$\Delta\ \epsilon\ $%s \n  (%s) [eV] \n vs. \n (%s) [eV]" %(pro_name,x_fname,y_fname)
    
    ax.text(0.14, 0.97, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props,ha='center')
    ax.hist(dis_raw,bins=20,range=[-3.0,3.0],histtype='bar')
    ax.set_xlim(-3.0,3.0)
    plt.savefig(lr_histogram)
###################################################











