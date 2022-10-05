# train sklearn
import models.sklearn as mskl
# train lightgbm
import models.lightgbm as lgbm

# metrics
import models.metrics as mt

# utils
import save_model as dm
import config_lib as cl
import models.dataset as ds
import models.features as fe


# get config info
config = cl.leer_config(".", "config")

# get train data and features
X_train, y_train, X_test, y_test = ds.read_prepare_dataset(config, 'SalePrice')
features = fe.read_selected_features(config,'LotFrontage')

# reduce the train and test set to the selected features
X_train = X_train[features]
X_test = X_test[features]

# train the models
mape = {}
metadata = {}
models = [mskl.train_sklearn, lgbm.train_lightgbm]
for model in models:
    algoritmo, model_name, hp, metrics = model(config, X_train, y_train, X_test, y_test)
    mape[algoritmo] = [d["numberValue"] for d in metrics["metrics"] if d["name"] == "train_mape"][0]
    metadata[algoritmo] = ({"model_name": model_name, "hp": hp, "metrics": metrics})

# choose model by min mse value
algoritmo_selected = min(mape, key=mape.get)
meta = metadata[algoritmo_selected]
model_name = meta["model_name"]
hp = meta["hp"]
metrics = meta["metrics"]

print()
print(f'algorithm selected: {algoritmo_selected}')
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

