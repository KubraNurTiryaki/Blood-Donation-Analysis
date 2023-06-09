# -*- coding: utf-8 -*-
"""BloodDonationAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19MBvUoHtmwtggMftLDfeEx7zTqTKIhZF
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np

#libraries for visualization

import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

#libraries for splitting model into train and test and for data transformation
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score

#filter the unwanted warning
import warnings
warnings.simplefilter("ignore")

#importinh all the required model for model comparison
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

"""Reading the Data"""

train = pd.read_csv("blood-train.csv")
test = pd.read_csv("blood-test.csv")

#print the traim and test size
print("Train shape: ", train.shape)
print("Test shape: ", test.shape)

#printhing first ten rows of data
train.head(10)

test.head()

#counting the num of people who donated and not donated
train["Made Donation in March 2007"].value_counts()

#storing dependent variable  in Y
Y = train.iloc[:,-1]
Y.head()

#printing last 10 rpws
train.tail(10)

#removing unnamed : 0 columns
old_train = train
train = train.iloc[:,1:5] #only 1,2,3,4 th columns there are anymore
test = test.iloc[:,1:5]

#printing first rows
train.head()

test.head()

#merging both train and test data
df = pd.merge(train,test)

df.head()
df.info()

#setting the independent variable and dependent variable
X = df.iloc[:,:]
X.head()

"""Data Exploartion"""

#Statistcs of the data
train.describe()

#bocplot for months since last donation
plt.figure(figsize=(20,10))
sns.boxplot(y = "Months since Last Donation", data = old_train)

"""We see from the above that the max people have donated blood in nearby 10 months

"""

#correlation between all variables [Checking how diffrent variable are related]
corrmat = X.corr()
f, ax = plt.subplots(figsize= (9,8))
sns.heatmap(corrmat, ax = ax, cmap ="YlGnBu", linewidths= 0.1, fmt =".2f", annot = True)

#printing all unique value for Month Since last donation
train["Months since Last Donation"].unique()

"""Feature Engineering
Volume donated is also a good feature to know whether the donor will donate or not
"""

#Creating new variable for calculating how many times a person have donated
X["Donating for"] = X["Months since First Donation"] - X["Months since Last Donation"]

#seeig first te rows of the DataFrame
X.head(10)

#correlatio betwee all variables
corrmat = X.corr()
f, ax = plt.subplots(figsize =(9,8))
sns.heatmap(corrmat, ax = ax, cmap ="YlGnBu", linewidths= 0.1, fmt =".2f", annot = True)

#dropping the unnecessary column
X.drop(["Total Volume Donated (c.c.)"], axis=1, inplace = True)
X.head()

#shape of independent variable
X.shape

"""Feature Transformation"""

#feature scaling
from sklearn.preprocessing import StandardScaler
scale = StandardScaler ()

#fitting and transforming data
X = scale.fit_transform(X)

train = X[:576]
train.shape

test = X[576:]

Y = Y[:576]
Y.shape

"""Model Building"""

#splitting into train and test set
xtrain, xtest, ytrain, ytest = train_test_split(train, Y , test_size = 0.2, random_state=18)

"""Steps to Follow
-Create the object
-Do the necessary hyperparameter tuning
-Fit the model
-Predict test set
-Compute roc_auc_score
-Repeat above step for all model
-Compare roz_auc_score of all model and choose the best model

Logisctic Regression
"""

#building the model 
logreg = LogisticRegression(random_state = 18)
#fitting the model
logreg.fit(xtrain,ytrain)

#predicting on the test data
pred = logreg.predict(xtest)

accuracy_score(pred, ytest)

#printing the roc_auc_score
roc_auc_score(pred, ytest)

"""Support Vector Machine"""

#SVC classifier
SVMC = SVC(probability = True)
#fitting the model
SVMC.fit(train, Y)

#predicting on the test data
pred = SVMC.predict(xtest)
accuracy_score(pred, ytest)

#printing the confusion matrix
confusion_matrix(pred, ytest)

roc_auc_score(pred, ytest)

"""Random Forest"""

#building the model
RFC = RandomForestClassifier()
RFC.fit(xtrain, ytrain)

#predicting the test data result
pred = RFC.predict(xtest)

# printing confusion matrix
confusion_matrix(pred,ytest)

accuracy_score(pred, ytest)

roc_auc_score(pred, ytest)

"""Decision Tree"""

model = DecisionTreeClassifier(max_leaf_nodes=4, max_features = 3, max_depth= 15)

model.fit(xtrain, ytrain)

pred = model.predict(xtest)

confusion_matrix(pred,ytest)

accuracy_score(pred, ytest)

roc_auc_score(pred, ytest)

"""MLP Classifier(multilayer perceptron classifier)"""

clf_neural = MLPClassifier(solver = "lbfgs", alpha = 1e-5, hidden_layer_sizes=(25,), random_state=18)
clf_neural.fit(train,Y)

predicted = clf_neural.predict(xtest)

confusion_matrix(predicted, ytest)

roc_auc_score(pred,ytest)

accuracy_score(pred, ytest)

