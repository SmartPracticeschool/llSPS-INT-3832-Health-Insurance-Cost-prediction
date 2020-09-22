# -*- coding: utf-8 -*-
"""health-insurance-cost-predicition (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jqmXZi6u-gvmF1m7dUFVM9plXZT8scis

# Prediction of Health Insurance Cost by Linear Regression

### Loading the libraries and modules
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import scipy as sp
import sklearn as sk
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn.model_selection import cross_val_score, KFold
from sklearn import model_selection
from sklearn import linear_model
from sklearn.metrics import mean_squared_error,mean_absolute_error

"""### Loading the data"""

from google.colab import files
uploaded = files.upload()
insurance = pd.read_csv('insurance.csv')
insurance.info()

"""#### First, we define a function to distinguish smokers and non-smokers"""

def map_smoking(column):
    mapped=[]
    
    for row in column:
        
        if row=="yes":
            mapped.append(1)
        else:
            mapped.append(0)
        
        
    return mapped
insurance["smoker_norm"]=map_smoking(insurance["smoker"])

nonnum_cols=[col for col in insurance.select_dtypes(include=["object"])]

"""#### Also, we will create a new feature that distinguishes obese and non-obese individuals"""

def map_obese(column):
    mapped=[]
    for row in column:
        if row>30:
            mapped.append(1)
        else:
            mapped.append(0)
    return mapped
insurance["obese"]=map_obese(insurance["bmi"])

insurance.head(5)

"""### We now explore the relation between the features given and the insurance costs"""

colnum=len(insurance.columns)-3
fig,ax=plt.subplots(colnum,1,figsize=(3,25))
ax[0].set_ylabel("charges")
p_vals={}
for ind,col in enumerate([i for i in insurance.columns if i not in ["smoker","region","charges","sex_norm"]]):
    
    ax[ind].scatter(insurance[col],insurance.charges,s=5)
    ax[ind].set_xlabel(col)
    ax[ind].set_ylabel("charges")    
plt.show()

corr_vals=[]
collabel=[]
for col in [i for i in insurance.columns if i not in nonnum_cols]:
    
    p_val=sp.stats.pearsonr(insurance[col],insurance["charges"])
    corr_vals.append(np.abs(p_val[0]))
    print(col,": ",np.abs(p_val[0]))
    collabel.append(col)
plt.bar(range(1,len(corr_vals)+1),corr_vals)
plt.xticks(range(1,len(corr_vals)+1),collabel,rotation=45)
plt.ylabel("Absolute correlation")

"""### Apparently, smoking, age and obesity are the factors that contribute the most in the calculation of insurance costs. We will only use those features for our predictions."""

cols_not_reg3=['age', 'obese', 'smoker_norm']

"""We will make our predictions using Linear Regression, for which we will model the relationship between the three variables and insurance costs  by fitting a linear equation to observed data. <br>
We will assume that the model for multiple linear regression, given n=3 observations, is : <br>
y = a*x1 + b*x2 + c*x3 + i <br>
where:<br>
y is the health insurance cost <br>
a is the age penalty <br>
b is the obesity penalty, while x2 will accept a value of 1 for obese individuals and 0 for non-obese ones. <br>
c is the penalty to smokers, for which x3 will have a value of 1 <br>
i is the intercept of the equation <br>

### We will make our predictions using K-fold cross validation
In k-fold cross-validation, we create the testing and training sets by splitting the data into **k** equally sized subsets. We then treat a single subsample as the testing set, and the remaining data as the training set. We then run and test models on all **k** datasets, and average the estimates. Let’s try it out with 10 folds and using Linear Regression:
"""

kf=KFold(n_splits=10, random_state=1, shuffle=True)
intercepts=[]
mses=[]
coefs=[]

for train_index, test_index in kf.split(insurance[cols_not_reg3]):
    
    lr=linear_model.LinearRegression()
    lr.fit(insurance[cols_not_reg3].iloc[train_index],insurance["charges"].iloc[train_index])
    lr_predictions=lr.predict(insurance[cols_not_reg3].iloc[test_index])
    
    lr_mse=mean_squared_error(insurance["charges"].iloc[test_index],lr_predictions)
    
    intercepts.append(lr.intercept_)
    
    coefs.append(lr.coef_)
    mses.append(lr_mse)

rmses=[x**.5 for x in mses]
avg_rmse=np.mean(rmses)
avg_intercept=np.mean(intercepts)
age_coefs=[]
obesity_coefs=[]
smoking_coefs=[]
for vals in coefs:
    #print vals[0]
    age_coefs.append(vals[0])
    obesity_coefs.append(vals[1])
    smoking_coefs.append(vals[2])
age_coef=np.mean(age_coefs)
obesity_coef=np.mean(obesity_coefs)
smoking_coef=np.mean(smoking_coefs)
print("a: ",age_coef," b: ",obesity_coef," c: ",smoking_coef," intercept: ",avg_intercept)

"""### After we obtain the LR coefficients, we define a function that will automatically predict a insurance cost value given age, obesity and smoking parameters"""

def calculate_insurance(age,obesity,smoking):
    y=(age_coef*age)+(obesity_coef*obesity)+(smoking_coef*smoking)+avg_intercept
    return y

"""### For example, a 34 year old, obese and smoker individual will have to pay the following price for his insurance:"""

print(calculate_insurance(34,1,1))