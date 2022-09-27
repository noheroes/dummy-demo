# base
import os
import json
from os import path

# to handle datasets
import pandas as pd
import numpy as np

# to pack the model
import joblib

# to build the model
from sklearn.linear_model import Lasso

# to evaluate the model
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt

import lightgbm as lgbm

# metrics
import metrics as mt

# utils
import s3_lib as s3l
import save_model as dm
import files_lib as fl
import config_lib as cl
import params_lib as pl


def create_metrics(
    train_mse,
    train_rmse,
    train_r2,
    test_mse,
    test_rmse,
    test_r2,
    average_house_price
):
    return {
        "metrics": [
            {
                "name": "train mse",
                "numberValue": train_mse,
                "format": "RAW"
            },
            {
                "name": "train rmse",
                "numberValue": train_rmse,
                "format": "RAW"
            },
            {
                "name": "train r2",
                "numberValue": train_r2,
                "format": "RAW"
            },
            {
                "name": "average house price",
                "numberValue": average_house_price,
                "format": "RAW"
            }
        ]
    }


def lee_s3(config, localpath, referencepath):
    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    prm_aws_access_key_id = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_access_key_id"),
        "El parametro access_key_id es obligatorio."
    )
    prm_aws_secret_access_key = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_secret_access_key"),
        "El parametro secret_access_key es obligatorio."
    )
    return s3l.readS3(prm_aws_endpoint,
                      prm_aws_access_key_id,
                      prm_aws_secret_access_key,
                      prm_aws_s3_bucket,
                      localpath,
                      referencepath)


def read_prepare_dataset(config):
    # to visualise al the columns in the dataframe
    pd.pandas.set_option('display.max_columns', None)

    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "dataset"),
            "la ruta remota para la data de entrenamiento es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "train"),
            "la ruta local para la data de entrenamiento es obligatoria.")
    archivo_train = pl.validar_parametros(
            cl.valor_config(config, "files", "train"),
            "el nombre del dataset de entrenamiento es obligatorio")
    nombre_local = path.join(localpath, archivo_train)
    nombre_remoto = path.join(remotepath, archivo_train)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    X_train = pd.read_csv(nombre_archivo)

    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "dataset"),
            "la ruta remota para la data de test es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "test"),
            "la ruta local para la data de test es obligatoria.")
    archivo_test = pl.validar_parametros(
            cl.valor_config(config, "files", "test"),
            "el nombre del dataset de test es obligatorio")
    nombre_local = path.join(localpath, archivo_test)
    nombre_remoto = path.join(remotepath, archivo_test)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    X_test = pd.read_csv(nombre_archivo)

    X_train.head()
    y_train = X_train['SalePrice']
    y_test = X_test['SalePrice']
    return X_train, y_train, X_test, y_test


def read_selected_features(config):
    file = 'features'
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", file),
            "la ruta remota para los features es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", file),
            "la ruta local para los features es obligatoria.")
    archivo_test = pl.validar_parametros(
            cl.valor_config(config, "files", file),
            "el nombre del archivo de features es obligatorio")
    nombre_local = path.join(localpath, archivo_test)
    nombre_remoto = path.join(remotepath, archivo_test)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    features = pd.read_csv(nombre_archivo)

    features = features['0'].to_list()
    features = features + ['LotFrontage']

    return features


def train_sklearn(config, X_train, y_train, X_test, y_test):
    algoritmo = 'sklearn'

    archivo_hp = os.path.join(
        pl.validar_parametros(
            cl.valor_config(config, "paths", "hyperparameters"),
            "la ruta para los hiper parametros es obligatoria."),
        pl.validar_parametros(
            cl.valor_config(config, "models", algoritmo, "hyperparameters"),
            "el nombre del archivo de hiper parametros es obligatorio.")
    )
    jparams = fl.leer_json(archivo_hp)
    hparams = json.dumps(jparams)

    alpha = jparams["hparams"]["alpha"]
    random_state = jparams["hparams"]["random_state"]

    # configure model
    lin_model = Lasso(alpha=alpha, random_state=random_state)

    # model fit
    lin_model.fit(X_train, y_train)

    # create the model
    archivo_modelo = "".join([
        pl.validar_parametros(
            cl.valor_config(config, "models", algoritmo, "name"),
            "el nombre del archivo del modelo es obligatorio."),
        pl.validar_parametros(
            cl.valor_config(config, "models", algoritmo, "extension"),
            "la extensión del archivo del modelo es obligatoria.")
    ])
    ruta_modelo = os.path.join(
        pl.validar_parametros(
            cl.valor_config(config, "paths", "models"),
            "la ruta del archivo del modelo es obligatoria."),
        archivo_modelo
    )
    joblib.dump(lin_model, ruta_modelo)

    # ====================
    # evaluate the model:
    # ====================

    # determine mse and rmse of train
    print(algoritmo)
    pred = lin_model.predict(X_train)
    trmse = int(mean_squared_error(np.exp(y_train), np.exp(pred)))
    print('train mse: {}'.format(trmse))
    trrmse = int(sqrt(mean_squared_error(np.exp(y_train), np.exp(pred))))
    print('train rmse: {}'.format(trrmse))
    trr2 = r2_score(np.exp(y_train), np.exp(pred))
    print('train r2: {}'.format(trr2))
    print()

    # determine mse and rmse of test
    print(algoritmo)
    pred = lin_model.predict(X_test)
    temse = int(mean_squared_error(np.exp(y_test), np.exp(pred)))
    print('test mse: {}'.format(temse))
    termse = int(sqrt(mean_squared_error(np.exp(y_test), np.exp(pred))))
    print('test rmse: {}'.format(termse))
    ter2 = r2_score(np.exp(y_test), np.exp(pred))
    print('test r2: {}'.format(ter2))
    print()

    # determine average house price
    ahp = int(np.exp(y_train).median())
    print('Average house price: ', ahp)
    print()

    metrics = create_metrics(trmse, trrmse, trr2, temse, termse, ter2, ahp)
    return algoritmo, archivo_modelo, hparams, metrics


# lightgbm
def train_lightgbm(config, X_train, y_train, X_test, y_test):
    algoritmo = 'lightgbm'

#    archivo_hp = os.path.join(
#        pl.validar_parametros(
#            cl.valor_config(config, "paths", "hyperparameters"),
#            "la ruta para los hiper parametros es obligatoria."),
#        pl.validar_parametros(
#            cl.valor_config(config, "models", algoritmo, "hyperparameters"),
#            "el nombre del archivo de hiper parametros es obligatorio")

#    jparams = fl.leer_json(archivo_hp)
#    hparams = json.dumps(jparams)

    hparams = {
         'task': 'train',
         'boosting_type': 'gbdt',
         'objective': 'regression',
         'num_leaves': 10,
         'learning_rate': 0.05,
         'metric': {'12', '11'},
         'verbose': -1
    }

    lgtrain = lgbm.Dataset(X_train, y_train)
    lgeval = lgbm.Dataset(X_test, y_test, reference=lgtrain)

    # model fit
    lgbm_model = lgbm.train(
                    hparams,
                    lgtrain,
                    num_boost_round=200,
                    valid_sets=[lgtrain, lgeval],
                    valid_names=['train', 'valid']
                )

    # create the model
    archivo_modelo = ''.join([
        pl.validar_parametros(
            cl.valor_config(config, "models", algoritmo, "name"),
            "el nombre del archivo del modelo es obligatorio."),
        pl.validar_parametros(
            cl.valor_config(config, "models", algoritmo, "extension"),
            "la extensión del archivo del modelo es obligatoria.")
    ])
    ruta_modelo = os.path.join(
        pl.validar_parametros(
            cl.valor_config(config, "paths", "models"),
            "la ruta del archivo del modelo es obligatoria."),
        archivo_modelo
    )
    joblib.dump(lgbm_model, ruta_modelo)

    # ====================
    # evaluate the model:
    # ====================

    # determine mse and rmse of train
    print(algoritmo)
    pred = lgbm_model.predict(X_train, num_iteration=lgbm_model.best_iteration)

    trmse = int(mean_squared_error(np.exp(y_train), np.exp(pred)))
    print('train mse: {}'.format(trmse))
    trrmse = int(sqrt(mean_squared_error(np.exp(y_train), np.exp(pred))))
    print('train rmse: {}'.format(trrmse))
    trr2 = r2_score(np.exp(y_train), np.exp(pred))
    print('train r2: {}'.format(trr2))
    print()

    # determine mse and rmse of test
    print(algoritmo)
    pred = pred = lgbm_model.predict(X_test, num_iteration=lgbm_model.best_iteration)
    temse = int(mean_squared_error(np.exp(y_test), np.exp(pred)))
    print('test mse: {}'.format(temse))
    termse = int(sqrt(mean_squared_error(np.exp(y_test), np.exp(pred))))
    print('test rmse: {}'.format(termse))
    ter2 = r2_score(np.exp(y_test), np.exp(pred))
    print('test r2: {}'.format(ter2))
    print()

    # determine average house price
    ahp = int(np.exp(y_train).median())
    print('Average house price: ', ahp)
    print()

    metrics = create_metrics(trmse, trrmse, trr2, temse, termse, ter2, ahp)
    return algoritmo, archivo_modelo, hparams, metrics


# get config info
config = cl.leer_config("..", "config")

# get train data and features
X_train, y_train, X_test, y_test = read_prepare_dataset(config)
features = read_selected_features(config)

# reduce the train and test set to the selected features
X_train = X_train[features]
X_test = X_test[features]

# train the models
mse = {}
metadata = {}
models = [train_sklearn, train_lightgbm]
for model in models:
    algoritmo, model_name, hp, metrics = model(config, X_train, y_train, X_test, y_test)
    mse[algoritmo] = [d["numberValue"] for d in metrics["metrics"] if d["name"] == "train mse"][0]
    metadata[algoritmo] = ({"model_name": model_name, "hp": hp, "metrics": metrics})

# choose model by min mse value
algoritmo_selected = min(mse, key=mse.get)
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
mt.save_metrics(metrics)

# save info in s3
dm.main(algoritmo_selected, model_name)

# save model selected

