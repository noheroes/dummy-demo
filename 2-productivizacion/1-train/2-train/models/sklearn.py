import os
import json
import joblib
import files_lib as fl
import files as f1
import models.metrics as mt

# to build the model
from sklearn.linear_model import Lasso

# to evaluate the model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

from math import sqrt
import numpy as np


def train_sklearn(config, X_train, y_train, X_test, y_test):
    algoritmo = 'sklearn'

    archivo_hp = os.path.join(
        f1.obtener_ruta(config, "paths", "hyperparameters",
            "la ruta para los hiper parametros es obligatoria."),
        f1.obtener_ruta2(config, "models", algoritmo, "hyperparameters",
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
    trmape = mean_absolute_percentage_error(y_train, pred)
    print('train mape: {}'.format(trmape))
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
    temape = mean_absolute_percentage_error(y_test, pred)
    print('train mape: {}'.format(temape))
    print()

    # determine average house price
    ahp = int(np.exp(y_train).median())
    print('Average house price: ', ahp)
    print()

    metrics = mt.create_metrics(trmse, trrmse, trr2, trmape, temse, termse, ter2, temape, ahp)
    return algoritmo, archivo_modelo, hparams, metrics
