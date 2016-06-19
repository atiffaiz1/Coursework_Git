% fid1=fopen('data.dat','wt');
% load lijianyicutl1
% for i=1:length(node_xyz)
%     fprintf(fid1,'%8.6f ',node_xyz(:,i)');
%         fprintf(fid1,'\n');
%     
% end
% fclose(fid1)

fid2=fopen('stent.dat','wt');
fid3=fopen('simplex.dat','wt')
load stent_03

for i=1:64
    for j=48

        fprintf(fid2,'%8.6f ',meshpoint1(i,j,1),meshpoint1(i,j,2),meshpoint1(i,j,3));
        fprintf(fid2,'\n');
                
    end
end
stent=load('stent.dat');
stent=stent(1:60,:)
stent=[stent;stent ;stent ;stent ;stent ;stent ;stent ;stent ;stent ;stent];
for i=1:600
    fprintf(fid3,'%f ', stent(i,:));
    fprintf(fid3,'\n');
end
fclose(fid3)
fclose(fid2)