import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

# !pip install yellowbrick
from yellowbrick.regressor import CooksDistance
from yellowbrick.datasets import load_concrete

# Concatenate tables of all vehicles containing travel time-duration to create only one bigger table
import glob
folder = 'D:\\work\\Dr Buzna\\R files\\data\\trips'
path = folder + "\\**\\Regression-sps-sp\\travel_time_regression.csv"
df = pd.concat(map(pd.read_csv, glob.iglob(path, recursive=True)))
print(type(df))
print(df.head())
print(df.columns)
print('number of points is: ',len(df['Duration']))
# Load the regression dataset
X = df[['Length_m']].values
y = df['Duration'].values
print(type(X))
print(len(y),len(X))
print(X)
y = df['Duration'].values
print(type(y))

# Instantiate and fit the visualizer
visualizer = CooksDistance()
visualizer.fit(X, y)
visualizer.show()

from sklearn.linear_model import LinearRegression
from yellowbrick.regressor import ResidualsPlot

# Instantiate and fit the visualizer
model = LinearRegression()
visualizer_residuals = ResidualsPlot(model)
visualizer_residuals.fit(X, y)
visualizer_residuals.show()

i_less_influential = (visualizer.distance_ <= visualizer.influence_threshold_)
X_li, y_li = X[i_less_influential], y[i_less_influential]

model = LinearRegression()
visualizer_residuals = ResidualsPlot(model)
visualizer_residuals.fit(X_li, y_li)
visualizer_residuals.show()

y = [i for _,i in sorted(zip(X_li,y_li))]
x = X_li
x_sorted = sorted(x)
x_sorted_40000 = [i for i in x_sorted if i < 40000]
y_sorted_40000 = y[0:len(x_sorted_40000)]
x = x_sorted_40000
y = y_sorted_40000

#     x = X_li.values
#     y = y_li.values
plt.style.use('seaborn')
plt.scatter(x,y,
            c=x,
            cmap=plt.cm.Reds,
#                 s=scatter_points["Duration"]*0.5,
            s=50,
            edgecolor='black',
           linewidth=0.75)
plt.xlabel('Distance (meter)')
plt.ylabel('Travel Time (min)')
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.colorbar()

#     plt.xscale('log')
#     plt.yscale('log')

#______________________Regression Model___________________#
# Find the Breaking point to split the regression model into two different types of regression (linear & non-linear)

breakpoint_list = []
rmse_list = []
LinRegCoeff_list = []
LinRegInterc_list = []
NonLinCoeff_list = []

for ff in range(3000,11000,100):

#     y = [i for _,i in sorted(zip(X_li['Length_m'].values,y_li))]
#     x = X_li[['Length_m']].values

#     x_sorted = sorted(x)
#     x_sorted_above = [i for i in x_sorted if i>ff]
#     y_above = y[-len(x_sorted_above):]
    x_sorted_above = [i for i in x_sorted_40000 if i>ff]
    y_above = y[-len(x_sorted_above):]

    X_train, X_test, y_train, y_test = train_test_split(x_sorted_above, y_above, test_size=0.2, random_state=0)

    regressor = LinearRegression()  
    regressor.fit(X_train, y_train) #training the algorithm

    #To retrieve the intercept:
#     print(regressor.intercept_)

    #For retrieving the slope:
#     print(regressor.coef_)
    
    y_pred = regressor.predict(X_test)

    # Root mean square error 
    RMSE1 = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
##########################################################################

#     y = [i for _,i in sorted(zip(X_li['Length_m'].values,y_li))]
#     x = X_li['Length_m'].values

#     x_sorted = sorted(x)
#     x_sorted_below = [i for i in x_sorted if i<ff]
#     y_below = y[0:len(x_sorted_below)]
    from sklearn.model_selection import train_test_split 
    from sklearn.linear_model import LinearRegression
    from sklearn import metrics
    from scipy.optimize import curve_fit

    xx = [float(d) for d in x_sorted_40000]
    x_sorted = sorted(xx)
    x_sorted_below = [i for i in x_sorted if i<ff]
    y_below = y[0:len(x_sorted_below)]

    # define the true objective function
    def objective(x,c):
        return c * np.sqrt(x)

#     x = x_sorted_below
#     y = y_below
    # curve fit
    popt, _ = curve_fit(objective, x_sorted_below, y_below)
    # summarize the parameter values
    c_fit = popt
    y_fit = c_fit * np.sqrt(x_sorted_below)
#     print(c_fit)
#     print('y = %0.5f * sqrt(x)' %(c_fit))

    RMSE2 =  np.sqrt(metrics.mean_squared_error(y_below, y_fit))
    
    breakpoint_list.append(ff)
    rmse_list.append(RMSE1+RMSE2)
    LinRegCoeff_list.append(regressor.coef_)
    LinRegInterc_list.append(regressor.intercept_)
    NonLinCoeff_list.append(c_fit)
    
    
breakpoint_star = min(zip(rmse_list,breakpoint_list))[1]
LinRegCoeff_star = min(zip(rmse_list,LinRegCoeff_list))[1]
LinRegInterc_star = min(zip(rmse_list,LinRegInterc_list))[1]
NonLinCoeff_star = min(zip(rmse_list,NonLinCoeff_list))[1]

print('rmse: ', min(rmse_list))
print('breakpoint_star: ', breakpoint_star)
# print('a: ', LinRegCoeff_star)
# print('b: ', LinRegInterc_star)
# print('c: ', NonLinCoeff_star)
print('y = %0.5f * sqrt(x)' %(c_fit))
print('y = %0.5f * x + %0.5f' %(LinRegCoeff_star,LinRegInterc_star))

#     print('The breakpoint is at x= ', ff)
#     print('Root Mean Squared Error "Linear Part":', RMSE1)
#     print('Root Mean Squared Error "NonLinear Part":', RMSE2)
#     print('Total Root Mean Square Error', RMSE1+RMSE2)
#     print('-----------------')

plt.plot(breakpoint_list, rmse_list, color = 'black')
z = min(zip(rmse_list,breakpoint_list))[1]
plt.plot(z,np.min(rmse_list), color = 'red')

plt.scatter(z, np.min(rmse_list), s=100, c='red', marker='o', cmap=None, norm=None,
            vmin=None, vmax=None, alpha=None, linewidths=None,)
plt.xlabel('Breakpoint')
plt.ylabel('RMSE')

#______________________Regression Line______________________#

# y = [i for _,i in sorted(zip(X_li['Length_m'].values,y_li))]
# x = X_li[['Length_m']].values
    
# x_sorted = sorted(x)
# x_sorted_below = [i for i in x_sorted if i < breakpoint_star]
# y_below = y[0:len(x_sorted_below)]
x_sorted_below = [i for i in x_sorted_40000 if i < breakpoint_star+200]
y_below = y[0:len(x_sorted_below)]
#----------
s = [i for _,i in sorted(zip(y_below,x_sorted_below))]
y_below_2x = sorted(y_below)
y_final_sort = [i for i in y_below_2x if i < 76]
x_final_sort = s[0:len(y_final_sort)]
#----------
plt.scatter(x_final_sort,y_final_sort, c='black',s=10)
x_line = np.arange(min(x_sorted_below), max(x_sorted_below), 1)
# calculate the output for the range
y_line = objective(x_line, NonLinCoeff_star)
# create a line plot for the mapping function
plt.plot(x_line, y_line, '--', color = 'red')
print(len(X_train))
print(len(y_below))
###################################
# y = [i for _,i in sorted(zip(X_li['Length_m'].values,y_li))]
# x = X_li[['Length_m']].values
    
# x_sorted = sorted(x)
# x_sorted_above = [i for i in x_sorted if i > breakpoint_star]
# y_above = y[-len(x_sorted_above):]
x_sorted_above = [i for i in x_sorted_40000 if i > breakpoint_star]
y_above = y[-len(x_sorted_above):]

print(len(x_sorted_above))
print(len(y_above))
plt.scatter(x_sorted_above,y_above, c='black',s=10)
y_pred = regressor.predict(X_test)
plt.plot(X_test, y_pred, '--', color='red', linewidth=2)
plt.xlabel('Distance (meter)')
plt.ylabel('Travel Time (min)')
