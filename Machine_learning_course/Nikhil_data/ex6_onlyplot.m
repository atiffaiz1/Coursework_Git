
%  This is a different dataset that you can use to experiment with. Try
%  different values of C and sigma here.
% 
file_name='ex6data3_try6.mat';
% Load from ex6data3: 
% You will have X, y in your environment
load(file_name);
k=60;
Error=[];

i=32;j=35;
        
        X=[X_g_norm(1:k,i) X_g_norm(1:k,j)];
        Xval=[X_g_norm(k+1:end,i) X_g_norm(k+1:end,j)];
        y=[y_g(1:k)];
        yval=[y_g(k+1:end)];
% Try different SVM Parameters here
        [C, sigma,error] = dataset3Params(X, y, Xval, yval);
        error
        Error=[error;Error];
% Train the SVM
        model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
        visualizeBoundary(X, y, model);
        i,j
%fprintf('Program paused. Press enter to continue.\n');

