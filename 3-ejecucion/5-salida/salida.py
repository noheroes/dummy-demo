# Import libraries
from os import path
import pandas as pd
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
            "el nombre del dataset de analytic es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    df_ad = pd.read_csv(nombre_archivo)
    return df_ad


def carga_predict(config):
    print("Cargando dataset de zona predict")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "predict_temp"),
            "la ruta remota para la data de predict_temp es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "predict_temp"),
            "la ruta local para la data de predict_temp es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "predict_temp"),
            "el nombre del dataset de predict_temp es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    df_ad = pd.read_csv(nombre_archivo)
    return df_ad


def prepare_salida(df_ad, df_predict):
    print("Preparando salida")
    df_ad['Probabilidad'] = df_predict
    return df_ad


def guardar_dataset(df_ad, config):
    print("Guardando salida")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "predict"),
            "la ruta remota para la data de predict es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "predict"),
            "la ruta local para la data de predict es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "predict"),
            "el nombre del dataset predict es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    df_ad.to_csv(nombre_local, index=False)
    escribe_s3(config, nombre_local, nombre_remoto)


def guardar_output(df_ad, config):
    print("Guardando output")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "output"),
            "la ruta remota para la data de output es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "output"),
            "la ruta local para la data de output es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "output"),
            "el nombre del dataset output es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    df_ad.to_csv(nombre_local, index=False)
    escribe_s3(config, nombre_local, nombre_remoto)


def inicio():
    # get config info
    config = cl.leer_config(".", "config")

    # get dataset
    df_ad = carga_dataset(config)
    # prepare dataset
    df_predict = carga_predict(config)
    # save dataset
    df_predict = prepare_salida(df_ad, df_predict)
    # save dataset
    guardar_dataset(df_predict, config)
    # save output
    guardar_output(df_predict, config)


if __name__ == "__main__":
    inicio()
