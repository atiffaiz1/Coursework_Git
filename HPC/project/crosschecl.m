X = [-0.172 -0.19  -0.17  -0.183 -0.166 -0.172 -0.189 -0.18  -0.212 -0.212 -0.205 -0.19  -0.187 -0.19  -0.198 -0.197]
Y =[-0.191 -0.21  -0.188 -0.202 -0.185 -0.191 -0.207 -0.199 -0.231 -0.231 -0.224 -0.21  -0.205 -0.208 -0.218 -0.216]
%scatter(X,Y)
hold on
%scatter(unnamed,unnamed1)
hold on
scatter(X_All,Y_All)
hold on

x = linspace(-0.16,-0.04,100);
c= 0.03469782;
m=  1.10698629;
y = m*x+c;

plot(x,y)