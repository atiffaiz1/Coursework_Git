function displaystentmesh(meshpoint,slice,raw,string)
for i=1:slice
        for j=1:raw
            
            if i==1 % 1st row (第1行)                
                if j==1
                  point1(1:3)=meshpoint(i,raw,:);
                else
                  point1(1:3)=meshpoint(i,j-1,:); 
                end
                
                 if j==raw
                    point2(1:3)=meshpoint(i,1,:);
                 else
                    point2(1:3)=meshpoint(i,j+1,:); 
                 end
                
                  point3(1:3)=meshpoint(i+1,j,:);
            end
               
              if i==slice % last row (第末行)                  
                if j==1
                  point1(1:3)=meshpoint(i,raw,:);
                else
                  point1(1:3)=meshpoint(i,j-1,:); 
                end
                
                 if j==raw
                    point2(1:3)=meshpoint(i,1,:);
                 else
                    point2(1:3)=meshpoint(i,j+1,:); 
                 end
                
                 point3(1:3)=meshpoint(i-1,j,:);
              end
             
              % the rest rows (from 2 to the last 2nd row) (其余2-倒数第二行)  
              if i>=2 && i<=slice-1
               if mod(i,2)==0   
                  if mod(j,2)==0 % even rows and even columns (双数行 双数列)
                        if j==raw
                           point3(1:3)=meshpoint(i,1,:);
                        else
                           point3(1:3)=meshpoint(i,j+1,:); 
                        end
                       point1(1:3)=meshpoint(i-1,j,:); 
                       point2(1:3)=meshpoint(i+1,j,:); 
                  else  % even rows and odd columns (双数行 单数列)
                      if j==1
                          point3(1:3)=meshpoint(i,raw,:);
                      else
                          point3(1:3)=meshpoint(i,j-1,:); 
                      end 
                      point1(1:3)=meshpoint(i-1,j,:); 
                      point2(1:3)=meshpoint(i+1,j,:); 
                  end
                  
               else  % odd rows (单数行)
                    if mod(j,2)==0 % odd rows and even columns (单数行 双数列)
                        if j==1
                           point3(1:3)=meshpoint(i,32,:);
                        else
                           point3(1:3)=meshpoint(i,j-1,:); 
                        end 
                        point1(1:3)=meshpoint(i-1,j,:); 
                        point2(1:3)=meshpoint(i+1,j,:);          
                      
                  else  % odd rows and odd columns (单数行 单数列)
                      if j==raw
                            point3(1:3)=meshpoint(i,1,:);
                      else
                           point3(1:3)=meshpoint(i,j+1,:); 
                      end
                      point1(1:3)=meshpoint(i-1,j,:); 
                      point2(1:3)=meshpoint(i+1,j,:); 
                  end
               end  
             end
    px=[meshpoint(i,j,1), point1(1)];
    py=[meshpoint(i,j,2), point1(2)];
    pz=[meshpoint(i,j,3), point1(3)];
    plot3(px,py,pz,string);
     hold on
    px=[meshpoint(i,j,1), point2(1)];
    py=[meshpoint(i,j,2), point2(2)];
    pz=[meshpoint(i,j,3), point2(3)];
    plot3(px,py,pz,string); 
    px=[meshpoint(i,j,1), point3(1)];
    py=[meshpoint(i,j,2), point3(2)];
    pz=[meshpoint(i,j,3), point3(3)];
    plot3(px,py,pz,string);
  end
end
    return
    
