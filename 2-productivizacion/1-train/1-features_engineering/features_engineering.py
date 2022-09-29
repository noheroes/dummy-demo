# import libraries
import pandas as pd
import numpy as np

# utils
import libs.config_lib as cl
import models.dataset as ds
import models.features as fe

# to build the models
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel

config = cl.leer_config('.', 'config')

target = 'SalePrice'
X_train, y_train, X_test, y_test = ds.read_prepare_dataset(config, target)

# drop unnecessary variables from our training and testing sets
X_train.drop(['Id', target], axis=1, inplace=True)
X_test.drop(['Id', target], axis=1, inplace=True)
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
fe.write_selected_features(config, pd.Series(selected_feats))
# print(pd.Series(selected_feats).dt())