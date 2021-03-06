import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer
import numpy as np

train = pd.read_csv("../data/train.csv")




from sklearn import preprocessing

# transform categoric labels into number
cat_labels = ['MSZoning','Street','Alley','LotShape','LandContour','Utilities',
              'LotConfig','LandSlope','Neighborhood','Condition1','Condition2',
              'BldgType','RoofStyle','HouseStyle','RoofMatl','Exterior1st',
              'Exterior2nd','MasVnrType','ExterQual','ExterCond','Foundation',
              'BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2',
              'Heating','HeatingQC','CentralAir','Electrical','KitchenQual',
              'Functional','FireplaceQu','GarageFinish','GarageType','GarageQual',
              'GarageCond','PavedDrive','PoolQC','Fence','MiscFeature','SaleType','SaleCondition']

le = preprocessing.LabelEncoder()
for features in cat_labels:
    le.fit(train[features])
    train[features] = le.transform(train[features])


#find & remove outliers in saleprice
low_salesprice = train["SalePrice"].quantile(q=0.25)
high_salesprice = train["SalePrice"].quantile(q=0.75)

IRQ = high_salesprice - low_salesprice
IRQ = IRQ * 1.5
outliers = high_salesprice + IRQ

# Remove outliers from sales price
outliers =  train[train["SalePrice"].gt(outliers)].index
for outlier in outliers:
    train.drop(outlier, inplace=True)


#separate features
data_features_train = train.drop("SalePrice", axis=1)
data_labels_train = train["SalePrice"]


#Handle missing values in Training Data Set
imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(data_features_train)
data_features_train = imp.transform(data_features_train)


# Create train test split
features_train, features_test, labels_train, labels_test = train_test_split(data_features_train, data_labels_train, test_size=0.25, random_state=42)

from sklearn.linear_model import Lasso
clf = Lasso(alpha=0.1)
clf.fit(features_train,labels_train)
predicted = clf.predict(features_test)

fig, ax = plt.subplots()
ax.scatter(labels_test, predicted)
ax.plot([labels_train.min(), labels_train.max()], [labels_train.min(), labels_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()

# The coefficients
print('Coefficients: \n'), dict(zip(train.columns, clf.coef_))
# The mean squared error
print "Mean sqared error", np.sqrt(np.mean((predicted-labels_test)**2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % clf.score(features_test, labels_test))

from sklearn.metrics import r2_score
print "R-squared Error",r2_score(predicted,labels_test)