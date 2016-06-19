clc;
k=0;
for i=1:34
    for j=i:34
        k=k+1;
        Error2(k,1)=Error(k);
        Error2(k,2)=i;
        Error2(k,3)=j;
        
    end
end
