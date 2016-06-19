import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
n_samples, n_features = 10, 1
np.random.seed(0)
y = np.random.randn(n_samples)
X = np.random.randn(n_samples, n_features)
print X
print y
clf = linear_model.SGDRegressor(alpha=0.01)
print clf.fit(X, y)

print clf.get_params(deep=True)

print clf.decision_function(X)
 
plt.plot(x,y,'ro')
plt.plot(clf.decision_function(X),y,'ro')
