from sklearn import linear_model
from scipy import stats
import numpy as np
import scipy

## credit: https://stackoverflow.com/questions/27928275/find-p-value-significance-in-scikit-learn-linearregression

### I have manullay tested with R values :-)
def calculte_p_values(X, y, lm):
  params = np.append(lm.intercept_,lm.coef_)
  predictions = lm.predict(X)

  newX = np.append(np.ones((len(X),1)), X, axis=1)
  MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

  var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
  sd_b = np.sqrt(var_b)
  ts_b = params/ sd_b

  p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-   len(newX[0])))) for i in ts_b]

  sd_b = np.round(sd_b,3)
  ts_b = np.round(ts_b,3)
  p_values = np.round(p_values,3)
  params = np.round(params,4)

  return p_values

