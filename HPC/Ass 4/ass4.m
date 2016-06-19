[X,Y] = meshgrid(0:.01:1);
Z = sin(X .* pi).*exp(-Y.*pi);
surf(X,Y,Z)