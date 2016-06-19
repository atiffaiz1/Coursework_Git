# -*- coding: utf-8 -*-

def sort_n_count(A,length):

    if length==1: 
        return A,0
    else:
        L=A[:length/2]
        R=A[length/2:]
        L_len=length/2
        R_len=length-L_len
        sorted_L, X = sort_n_count(L,L_len)
        sorted_R, Y = sort_n_count(R,R_len)
        sorted_A, Z = merge_n_countsplit(sorted_L,sorted_R,L_len,R_len)
    return sorted_A, X+Y+Z
    
def merge_n_countsplit(L,R,L_len,R_len):
    i=0
    j=0
    count=0
    sorted_l=[]
    while i < L_len and j < R_len:
        if L[i]<=R[j]: 
            sorted_l.append(L[i])            
            i=i+1 
        else:
            sorted_l.append(R[j])   
            j=j+1
            count= count + (L_len-i)
    while i < L_len:
        sorted_l.append(L[i])
        i=i+1
    while j < R_len:
        sorted_l.append(R[j])
        j=j+1  
    return sorted_l,count

value_file=open('IntegerArray.txt')
values=[]
for lines in value_file:
    values.append(int(lines))
a=values
length=len(a)
print sort_n_count(a,length)[1]