import os
import joblib
import libs.files as f1
import models.metrics as mt

# to build the model
import lightgbm as lgbm

# to evaluate the model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

from math import sqrt
import numpy as np


# lightgbm
def train_lightgbm(config, X_train, y_train, X_test, y_test):
    algoritmo = 'lightgbm'

#    archivo_hp = os.path.join(
#        f1.obtener_ruta(config, "paths", "hyperparameters",
#            "la ruta para los hiper parametros es obligatoria."),
#        f1.obtener_ruta(config, "models", algoritmo, "hyperparameters",
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
        f1.obtener_ruta2(config, "models", algoritmo, "name",
            "el nombre del archivo del modelo es obligatorio."),
        f1.obtener_ruta2(config, "models", algoritmo, "extension",
            "la extensión del archivo del modelo es obligatoria.")
    ])
    ruta_modelo = os.path.join(
        f1.obtener_ruta(config, "paths", "models",
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
    trmape = mean_absolute_percentage_error(y_train, pred)
    print('train mape: {}'.format(trmape))
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
    temape = mean_absolute_percentage_error(y_test, pred)
    print('train mape: {}'.format(temape))
    print()

    # determine average house price
    ahp = int(np.exp(y_train).median())
    print('Average house price: ', ahp)
    print()

    metrics = mt.create_metrics(trmse, trrmse, trr2, trmape, temse, termse, ter2, temape, ahp)
    return algoritmo, archivo_modelo, hparams, metrics
