function [point1,point2,point3]=findneighbor(slice,raw,meshpoint)


% Search 3 neighboring points of the stent point (寻找支架点的3邻点)
for i=1:slice
    for j=1:raw
                 if i==1 % the 1st row (第1行)                
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
               
                 if i==slice % the last row (第末行)                  
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
             
                 % the rest rows (from 2 to the last 2nd row) (其余2-倒数第二行)  
                 if i>=2 && i<=slice-1
                    if mod(i,2)==0   
                       if mod(j,2)==0 % even rows and even columns (双数行 双数列)
                          if j==raw
                              point3(i,j,1:3)=meshpoint(i,1,:);
                          else
                             point3(i,j,1:3)=meshpoint(i,j+1,:); 
                          end
                         point1(i,j,1:3)=meshpoint(i-1,j,:); 
                         point2(i,j,1:3)=meshpoint(i+1,j,:); 
                      else  % even rows and odd columns (双数行 单数列)
                        if j==1
                            point3(i,j,1:3)=meshpoint(i,raw,:);
                        else
                          point3(i,j,1:3)=meshpoint(i,j-1,:); 
                        end 
                        point1(i,j,1:3)=meshpoint(i-1,j,:); 
                        point2(i,j,1:3)=meshpoint(i+1,j,:); 
                      end
                  
                 else  % odd rows (单数行)
                    if mod(j,2)==0 % odd rows and even columns (单数行 双数列)
                        if j==1
                           point3(i,j,1:3)=meshpoint(i,raw,:);
                        else
                           point3(i,j,1:3)=meshpoint(i,j-1,:); 
                        end 
                        point1(i,j,1:3)=meshpoint(i-1,j,:); 
                        point2(i,j,1:3)=meshpoint(i+1,j,:);          
                      
                   else  % odd rows and odd columns (单数行 单数列)
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
   % Finish searching 3 neighboring points (寻找3邻点结束) 