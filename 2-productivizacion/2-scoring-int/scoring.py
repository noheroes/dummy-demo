# Import libraries
import json
from os import path

import pandas as pd
import gc
import joblib

import files_lib as fl
import s3_lib as s3l
import config_lib as cl
import params_lib as pl


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


def escribe_s3(config, localpath, referencepath):
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
    return s3l.uploadS3(prm_aws_endpoint,
                 prm_aws_access_key_id,
                 prm_aws_secret_access_key,
                 prm_aws_s3_bucket,
                 localpath,
                 referencepath)


def leer_algoritmo_selected(parametrosScoring):
    rutaArchivoLocal = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_Model_Selected"),
        "La ruta del archivo del modelo seleccionado no puede ser nula"
    )
    rutaArchivoRemoto = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3paths", "Ruta_Model_Selected"),
        "La ruta del archivo del modelo seleccionado no puede ser nula"
    )
    nombreArchivo = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_Model_Selected"),
        "La nombre del archivo del modelo seleccionado no puede ser nula"
    )
    archivo_local = path.join(rutaArchivoLocal, nombreArchivo)
    archivo_remoto = path.join(rutaArchivoRemoto, nombreArchivo)
    archivo = lee_s3(parametrosScoring, archivo_local, archivo_remoto)
    info = fl.leer_json(archivo)
    algoritmo_selected = fl.valor_json(info, "algoritmo_selected")
    print(f'algoritmo_selected: {algoritmo_selected}')
    return algoritmo_selected


def carga_dataset(parametrosScoring):
    pd.pandas.set_option('display.max_columns', None)
    print("Cargando dataset de zona raw")
    rutaArchivoLocal = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_Analytic_Data"),
        "La ruta raw del archivo de parametros no puede ser nula"
    )
    rutaArchivoRemoto = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3paths", "Ruta_Analytic_Data"),
        "La ruta raw del archivo de parametros no puede ser nula"
    )
    nombreArchivo = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_Analytic_Data"),
        "La ruta raw del archivo de parametros no puede ser nula"
    )
    dataset_local = path.join(rutaArchivoLocal, nombreArchivo)
    dataset_remoto = path.join(rutaArchivoRemoto, nombreArchivo)

    archivo = lee_s3(parametrosScoring, dataset_local, dataset_remoto)
    df_ad = pd.read_csv(archivo)
    return df_ad


def carga_modelo(parametrosScoring, parametrosModelo):
    print("Cargando modelo de bucket")
    nombreModelo = pl.validar_parametros(
        cl.valor_config(parametrosModelo, "name", "Name_Model"),
        "El nombre del modelo no puede ser nulo"
    )
    rutaModeloRemoto = pl.validar_parametros(
        cl.valor_config(parametrosModelo, "paths", "Ruta_Model"),
        "La ruta del modelo no puede ser nula"
    )
    rutaModeloLocal = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_Model"),
        "La ruta del modelo no puede ser nula"
    )
    modelo_local = path.join(rutaModeloLocal, nombreModelo)
    modelo_remoto = path.join(rutaModeloRemoto, nombreModelo)

    nombreModelo = lee_s3(parametrosScoring, modelo_local, modelo_remoto)
    return nombreModelo


def carga_features(parametrosScoring):
    print("Leyendo Features")
    nombreFeatures = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_Features"),
        "El nombre de las features no puede ser nulo"
    )
    rutaFeaturesLocal = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_Features"),
        "La ruta de las features no puede ser nula"
    )
    rutaFeaturesRemoto = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3paths", "Ruta_Features"),
        "La ruta de las features no puede ser nula"
    )
    features_local = path.join(rutaFeaturesLocal, nombreFeatures)
    features_remoto = path.join(rutaFeaturesRemoto, nombreFeatures)
    nombreFeatures = lee_s3(parametrosScoring, features_local, features_remoto)
    df_features = pd.read_csv(nombreFeatures)
    df_features = df_features['0'].to_list()
    df_features = df_features + ['LotFrontage']

    return df_features


def scoring(df_ad, features, modelo):
    print("Ejecutando Scoring")

    # Load model
    model = joblib.load(modelo)
    data = df_ad[features]
    pred = df_ad

    # Execute model
    predict = model.predict(data, num_iteration=model.best_iteration)

    pred['predict'] = predict
    pred = pred[['Id', 'predict']]

    gc.collect()
    return pd.DataFrame(data=pred, index=None)


def guardar_salida(predict, parametrosScoring) -> str:
    print("Guardando salida")
    rutaSalidaLocal = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_PredictTemp_Data"),
        "La ruta del archivo de salida no puede ser nula"
    )
    rutaSalidaRemoto = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3paths", "Ruta_PredictTemp_Data"),
        "La ruta del archivo de salida no puede ser nula"
    )
    nombreSalida = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_PredictTemp_Data"),
        "El nombre del archivo de salida no puede ser nulo"
    )
    salida_local = path.join(rutaSalidaLocal, nombreSalida)
    salida_remoto = path.join(rutaSalidaRemoto, nombreSalida)
    predict.to_csv(salida_local)
    salida = escribe_s3(parametrosScoring, salida_local, salida_remoto)
    return salida


def convierte_dataset(data, parametrosScoring):
    data = json.loads(data)
    data = data["data"]
    print("Convirtiendo json a dataset")
    rutaArchivoLocal = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_Analytic_Data"),
        "La ruta raw del archivo de parametros no puede ser nula"
    )
    nombreArchivo = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_Analytic_Data"),
        "La ruta raw del archivo de parametros no puede ser nula"
    )
    dataset_local = path.join(rutaArchivoLocal, nombreArchivo)

    df_ad = pd.DataFrame.from_records(data)
    print(df_ad)
    return df_ad


def prepara_salida(predict, parametrosScoring):
    return predict.to_json(orient="records")


def inicio(data):
    # get config info
    parametrosScoring = cl.leer_config(".", "config")
    algoritmo_selected = leer_algoritmo_selected(parametrosScoring)
    # get dataset
    df_ad = convierte_dataset(data, parametrosScoring)
    # get features
    features = carga_features(parametrosScoring)
    # get model
    parametrosModelo = cl.leer_config(".", f"config_{algoritmo_selected}")
    nombreModelo = carga_modelo(parametrosScoring, parametrosModelo)
    # execute model
    df_predict = scoring(df_ad, features, nombreModelo)
    # save predict
    salida = prepara_salida(df_predict, parametrosScoring)
    return salida


if __name__ == "__main__":
    inicio()