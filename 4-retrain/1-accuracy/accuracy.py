import json
import numpy as np
import pandas as pd
from os import path
from sklearn.metrics import mean_absolute_percentage_error

import models.metrics as mt
import models.model as mdl
import models.predict as prd
import models.real as re
import libs.config_lib as cl
import libs.files as fl
import libs.s3 as s3


def leer_metrics(config, algoritmo_selected):
    metrics = mt.read_metrics(config, algoritmo_selected)
    train_mape = [d["numberValue"] for d in metrics["metrics"] if d["name"] == "train_mape"][0]
    return train_mape


def obtener_ratios(config):
    ratios = config["ratios"]
    print(f'ratios: {ratios}')
    return ratios


def obtener_metrica_evaluada(config):
    # Agregar logica para recibir data resutalte.
    df_predict = prd.leer_predict(config)
    df_real = re.leer_real(config)

    # Separamos columnas relevantes
    df_predict = df_predict[["Id", "predict"]]
    print("data predict")
    print(df_predict.head())
    print()
    df_real = df_real[["Id", "resultado"]]
    print("data results")
    print(df_real.head())
    print()

    # Realizamos un marge entre los 02 dataset
    df_merged_inner = pd.merge(df_predict, df_real)

    # Separamos las columnas a comparar
    y_true = df_merged_inner["resultado"]
    y_pred = df_merged_inner["predict"]
    
    mape_evaluado = mean_absolute_percentage_error(y_true, y_pred)
    return mape_evaluado
    

def evalua_metricas(mape_entrenado, mape_evaluado, ratios):
    # Comparación
    min_evaluado = min(mape_entrenado, mape_evaluado)
    max_evaluado = max(mape_entrenado, mape_evaluado)

    # Lógica de evaluación
    if mape_evaluado < mape_entrenado:
        dif = 0
    else:
        print(f"Metrica entrenada mape : {mape_entrenado}")
        print(f"Metrica evaluada mape  : {mape_evaluado}")
        dif = max_evaluado - min_evaluado
        print(f"Diferencia porcentual : % {dif*100}")

    if dif < ratios['recalibra']:
        accion = 0
        descripcion = "Ok"
        result = {"accion": accion, "descripcion": descripcion}
    elif dif < ratios['reentrena']:
        accion = 1
        descripcion = "Recalibra"
        result = {"accion": accion, "descripcion": descripcion}
    else:
        accion = 2
        descripcion = "Reentrenar"
        print("Acción requerida : Reentrenamiento ")
        result = {"accion": accion, "descripcion": descripcion}
    return json.dumps(result)


def guardar_salida(config, accuracy):
    localpath = fl.obtener_ruta(config, "paths", "accuracy", 
                                "La ruta local del accuracy es obligatoria.")
    remotepath = fl.obtener_ruta(config, "s3paths", "accuracy", 
                                 "La ruta remota del accuracy es obligatoria.")
    filename = fl.obtener_ruta(config, "files", "accuracy", 
                               "El nombre del archivo accuracy es obligatorio.")
    localfile = path.join(localpath, filename)
    remotefile = path.join(remotepath, filename)
    fl.guardar_json(localfile, accuracy)
    s3.escribe_s3(config, localfile, remotefile)


def main():
    config = cl.leer_config('.', 'config')
    algoritmo_selected = mdl.leer_algoritmo_selected(config)
    print(f'algoritmo_selected: {algoritmo_selected}')
    mape_entrenado = leer_metrics(config, algoritmo_selected)
    mape_evaluado = obtener_metrica_evaluada(config)
    ratios = obtener_ratios(config)
    accuracy = evalua_metricas(mape_entrenado, mape_evaluado, ratios)
    guardar_salida(config, accuracy)
    return accuracy


main()