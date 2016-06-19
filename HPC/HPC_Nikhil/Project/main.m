 clc;
 clear;
load lijianyicutl1

load stent_03
% figure
% axis equal

% patch('faces',face_node','vertices',node_xyz');
% 
%  alpha(0);
% color cool;

elapsed_time=[];
number_of_points=[];

raw=48;
slice=length(meshpoint1(:,1,:));
length_c=0.37*2;

arfa=0.1;
beta=0.1;
ax=0.4;
epsl=0.6;
scale=0.5;


meshpoint=meshpoint1;
% plot3(meshpoint(:,:,1),meshpoint(:,:,2),meshpoint(:,:,3),'g');
% hold on 


point_num_old=0;

d_one=zeros(slice,raw);
          tic
for n=1:1

    n

     point_num=0;% record the number of stent points that are in contact with 
     % the vessel within one loop (记录一个循环中和血管壁贴合的支架点数)
     errorpoint_num=0;% record the number of error points within one loop 
     % (记录一个循环中错误的点数)
     
    % Find the 3 neighboring nodes (寻找3邻点)
    [point1,point2,point3]=findneighbor(slice,raw,meshpoint);  
    % Calculate angle force and strut length force (计算角度和长度约束力)
    [flength,fangle]=com_flength_fangle_ling(meshpoint,length_c,raw,slice);
    
    
    for i=1:slice
        for j=1:raw
            stentpoint(1:3)=meshpoint(i,j,1:3);   

           distance=zeros(face_num,1);
            parfor k=1:face_num

        tri=[node_xyz(:,(k-1)*3+1)';node_xyz(:,(k-1)*3+2)';node_xyz(:,(k-1)*3+3)'];
        
   %distance(k)=dist;
   distance(k)=pointTriangleDistance(tri,stentpoint);
            end
%             if n==1
%                 d_one(i,j)=min(distance);
%             end
            d=min(distance);
%             disp(d);
            elapsed_time(end+1)=toc
            number_of_points(end+1)=(i-1)*48 + j;         


              
              sign=1;
              stent_center_distance=sqrt((meshpoint(i,j,1)-center(i,1))...
                 *(meshpoint(i,j,1)-center(i,1))+(meshpoint(i,j,2)-...
                 center(i,2))*(meshpoint(i,j,2)-center(i,2))+...
                 (meshpoint(i,j,3)-center(i,3))*(meshpoint(i,j,3)...
                 -center(i,3)));  
            
             % Calculate the expansion coefficient (计算膨胀系数)
             if  stent_center_distance>0
                dx=(meshpoint(i,j,1)-center(i,1))/stent_center_distance;
                dy=(meshpoint(i,j,2)-center(i,2))/stent_center_distance;
                dz=(meshpoint(i,j,3)-center(i,3))/stent_center_distance;
             else 
                     
                dx=0;
                dy=0;
                dz=0;
             end
            % Update the position of stent point (更新支架点的位置)
            newmeshpoint(i,j,1)=meshpoint(i,j,1)+arfa*(point1(i,j,1)/3+...
                point2(i,j,1)/3+point3(i,j,1)/3-meshpoint(i,j,1)+...
                ax*flength(i,j,1)+epsl*fangle(i,j,1))+beta*scale*...
                meshpoint(i,j,1)*sign*dx; 
         
            newmeshpoint(i,j,2)=meshpoint(i,j,2)+arfa*(point1(i,j,2)/3+...
               point2(i,j,2)/3+point3(i,j,2)/3-meshpoint(i,j,2)+...
               ax*flength(i,j,2)+epsl*fangle(i,j,2))+beta*scale*...
               meshpoint(i,j,2)*sign*dy;
         
            newmeshpoint(i,j,3)=meshpoint(i,j,3)+arfa*(point1(i,j,3)/3+...
               point2(i,j,3)/3+point3(i,j,3)/3-meshpoint(i,j,3)+...
               ax*flength(i,j,3)+epsl*fangle(i,j,3))+beta*scale*...
               meshpoint(i,j,3)*sign*dz;

              

         
        end
    end
meshpoint=newmeshpoint; 
         
  
           
          

     
end
% plot3(meshpoint(:,:,1),meshpoint(:,:,2),meshpoint(:,:,3),'r');
% hold on;

