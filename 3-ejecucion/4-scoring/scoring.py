# Import libraries
import gc
from os import path
import pandas as pd
import s3_lib as s3l
import config_lib as cl
import params_lib as pl
import os
import joblib


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
    s3l.uploadS3(prm_aws_endpoint,
                 prm_aws_access_key_id,
                 prm_aws_secret_access_key,
                 prm_aws_s3_bucket,
                 localpath,
                 referencepath)


def carga_dataset(config):
    print("Cargando dataset de zona analytic")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "analytic"),
            "la ruta remota para la data de analytic es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "analytic"),
            "la ruta local para la data de analytic es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "analytic"),
            "el nombre del dataset de entrenamiento es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    df_ad = pd.read_csv(nombre_archivo)
    return df_ad


def carga_features(config):
    print("Cargando dataset de features")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "features"),
            "la ruta remota para la data de features es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "features"),
            "la ruta local para la data de features es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "features"),
            "el nombre del dataset de entrenamiento es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    df_ad = pd.read_csv(nombre_archivo)
    return df_ad


def carga_modelo(config):
    print("Cargando modelo")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "model"),
            "la ruta remota para del model es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "model"),
            "la ruta local para del model es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "model"),
            "el nombre del modelo es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    return nombre_archivo


def scoring(df_ad, features, modelo):
    print("Ejecutando Scoring")

    # Load model
    model = joblib.load(modelo)

    # features
    features = features['0'].to_list() + ['LotFrontage']

    # Execute model
    predict = pd.DataFrame(model.predict(df_ad[features]))
    gc.collect()

    return predict


def guardar_dataset(df_ad, config):
    print("Guardando salida")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "predict_temp"),
            "la ruta remota para la data de input es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "predict_temp"),
            "la ruta local para la data de input es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "predict_temp"),
            "el nombre del dataset de entrenamiento es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    df_ad.to_csv(nombre_local, index=False)
    escribe_s3(config, nombre_local, nombre_remoto)


def inicio():
    # get config info
    algoritmo = os.getenv("ALGORITMO")
    archivo_config = f"config_{algoritmo}"
    config = cl.leer_config(".", archivo_config)

    # get dataset
    df_ad = carga_dataset(config)
    # get features
    features = carga_features(config)
    # get model
    nombreModelo = carga_modelo(config)
    # execute model
    df_predict = scoring(df_ad, features, nombreModelo)
    # save predict
    guardar_dataset(df_predict, config)


if __name__ == "__main__":
    inicio()
