import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import Imputer
from sklearn.linear_model import LinearRegression
import seaborn as sns
import numpy as np
from math import sqrt



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

# Transform categorical features to numerical
le = preprocessing.LabelEncoder()
for features in cat_labels:
    le.fit(train[features])
    train[features] = le.transform(train[features])


#Find correlation
corrolations = train.corr()['SalePrice'][:-1]
golden_feature_list = corrolations[abs(corrolations) > 0.5].sort_values(ascending = False)
print("There is {} strongly correlated values with SalePrice:\n{}".format(len(golden_feature_list), golden_feature_list))



#separate features
data_features_train = train.drop("SalePrice", axis=1)
# select top 8 features that are highly corrolated with sales price
data_features_train = data_features_train.filter(["OverallQual", "GrLivArea", "GarageCars",
                                                  "GarageArea", "TotalBsmtSF", "1stFlrSF",
                                                  "FullBath", "TotRmsAbvGrd","YearRemodAdd",
                                                  ],axis=1)

data_labels_train = train["SalePrice"]



#Handle missing values in Training Data Set
imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(data_features_train)
data_features_train = imp.transform(data_features_train)


# Create train test split
features_train, features_test, labels_train, labels_test = train_test_split(data_features_train, data_labels_train, test_size=0.25, random_state=42)


lr = LinearRegression()
lr.fit(features_train, labels_train)

# Train the model using the training sets
predicted = lr.predict(features_test)


# The coefficients
print('Coefficients: \n', lr.coef_)
# The mean squared error
print "Mean sqared error", np.sqrt(np.mean((predicted-labels_test)**2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % lr.score(features_test, labels_test))
from sklearn.metrics import r2_score
print "R-squared Error",r2_score(predicted,labels_test)

#Regression plot
sns.regplot(x = labels_test ,  y = predicted ,  data= train)
plt.show()


