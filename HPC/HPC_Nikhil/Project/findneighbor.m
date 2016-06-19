function [point1,point2,point3]=findneighbor(slice,raw,meshpoint)


% Search 3 neighboring points of the stent point (Ѱ��֧�ܵ��3�ڵ�)
for i=1:slice
    for j=1:raw
                 if i==1 % the 1st row (��1��)                
                      if j==1
                          point1(i,j,1:3)=meshpoint(i,raw,:);
                      else
                           point1(i,j,1:3)=meshpoint(i,j-1,:); 
                      end
                
                     if j==raw
                           point2(i,j,1:3)=meshpoint(i,1,:);
                     else
                           point2(i,j,1:3)=meshpoint(i,j+1,:); 
                     end
                
                     point3(i,j,1:3)=meshpoint(i+1,j,:);
                 end
               
                 if i==slice % the last row (��ĩ��)                  
                     if j==1
                        point1(i,j,1:3)=meshpoint(i,raw,:);
                     else
                        point1(i,j,1:3)=meshpoint(i,j-1,:); 
                     end
                
                     if j==raw
                        point2(i,j,1:3)=meshpoint(i,1,:);
                     else
                        point2(i,j,1:3)=meshpoint(i,j+1,:); 
                     end
                
                     point3(i,j,1:3)=meshpoint(i-1,j,:);
                 end
             
                 % the rest rows (from 2 to the last 2nd row) (����2-�����ڶ���)  
                 if i>=2 && i<=slice-1
                    if mod(i,2)==0   
                       if mod(j,2)==0 % even rows and even columns (˫���� ˫����)
                          if j==raw
                              point3(i,j,1:3)=meshpoint(i,1,:);
                          else
                             point3(i,j,1:3)=meshpoint(i,j+1,:); 
                          end
                         point1(i,j,1:3)=meshpoint(i-1,j,:); 
                         point2(i,j,1:3)=meshpoint(i+1,j,:); 
                      else  % even rows and odd columns (˫���� ������)
                        if j==1
                            point3(i,j,1:3)=meshpoint(i,raw,:);
                        else
                          point3(i,j,1:3)=meshpoint(i,j-1,:); 
                        end 
                        point1(i,j,1:3)=meshpoint(i-1,j,:); 
                        point2(i,j,1:3)=meshpoint(i+1,j,:); 
                      end
                  
                 else  % odd rows (������)
                    if mod(j,2)==0 % odd rows and even columns (������ ˫����)
                        if j==1
                           point3(i,j,1:3)=meshpoint(i,raw,:);
                        else
                           point3(i,j,1:3)=meshpoint(i,j-1,:); 
                        end 
                        point1(i,j,1:3)=meshpoint(i-1,j,:); 
                        point2(i,j,1:3)=meshpoint(i+1,j,:);          
                      
                   else  % odd rows and odd columns (������ ������)
                      if j==raw
                            point3(i,j,1:3)=meshpoint(i,1,:);
                      else
                           point3(i,j,1:3)=meshpoint(i,j+1,:); 
                      end
                      point1(i,j,1:3)=meshpoint(i-1,j,:); 
                      point2(i,j,1:3)=meshpoint(i+1,j,:); 
                  end
               end  
         end
              
    end
end
   % Finish searching 3 neighboring points (Ѱ��3�ڵ����) 