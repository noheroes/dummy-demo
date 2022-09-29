# train sklearn
import models.sklearn as mskl
# train lightgbm
import models.lightgbm as lgbm

# metrics
import models.metrics as mt

# utils
import save_model as dm
import libs.config_lib as cl
import models.dataset as ds
import models.features as fe
import models.model as mdl


# get config info
config = cl.leer_config(".", "config")

# get selected algorithm
algoritmo_selected = mdl.leer_algoritmo_selected(config)
print(f'algoritmo_selected: {algoritmo_selected}')

# get train data and features
X_train, y_train, X_test, y_test = ds.read_prepare_dataset(config, 'SalePrice')
features = fe.read_selected_features(config)

# reduce the train and test set to the selected features
X_train = X_train[features]
X_test = X_test[features]

# train the models
if algoritmo_selected == "sklearn":
    algoritmo, model_name, hp, metrics = mskl.train_sklearn(config, X_train, y_train, X_test, y_test)
else:
    algoritmo, model_name, hp, metrics = lgbm.train_lightgbm(config, X_train, y_train, X_test, y_test)

print()
print(f'algorithm: {algoritmo}')
print()
print(f'model: {model_name}')
print()
print(f'hp: {hp}')
print()
print(f'metrics: {metrics["metrics"]}')
print()

# save metrics
mt.save_metrics(config, metrics)

# save info in s3
dm.main(algoritmo_selected, model_name)
