# import libraries
import pandas as pd
import numpy as np

# utils
import s3_lib as s3l
import save_model as dm
import files_lib as fl
import config_lib as cl
import params_lib as pl

# to build the models
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel




# to visualise al the columns in the dataframe
pd.pandas.set_option('display.max_columns', None)



def read_data(input1_path):
    csv_data = pd.read_csv(input1_path, error_bad_lines=False)
    return csv_data


# read data
X_train = pd.read_csv('./xtrain.csv')
X_test = pd.read_csv('./xtest.csv')

X_train.head()

# remove duplicate rows
print(X_train.head())
# capture the target (remember that the target is log transformed)
y_train = X_train['SalePrice']
y_test = X_test['SalePrice']

# drop unnecessary variables from our training and testing sets
X_train.drop(['Id', 'SalePrice'], axis=1, inplace=True)
X_test.drop(['Id', 'SalePrice'], axis=1, inplace=True)
sel_ = SelectFromModel(Lasso(alpha=0.005, random_state=0))

# train Lasso model and select features
sel_.fit(X_train, y_train)
print(sel_.get_support())
selected_feats = X_train.columns[(sel_.get_support())]

# let's print some stats
print('total features: {}'.format((X_train.shape[1])))
print('selected features: {}'.format(len(selected_feats)))
print('features with coefficients shrank to zero: {}'.format(
    np.sum(sel_.estimator_.coef_ == 0)))

# save features
print(selected_feats)
selected_feats = X_train.columns[(sel_.estimator_.coef_ != 0).ravel().tolist()]
pd.Series(selected_feats).to_csv('./selected_features.csv', index=False)
print(pd.Series(selected_feats).dt())
