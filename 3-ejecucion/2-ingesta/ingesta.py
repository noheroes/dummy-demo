# Import libraries
from os import path
import pandas as pd
import s3_lib as s3l
import config_lib as cl
import params_lib as pl


def lee_s3(config, localpath, referencepath):
    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_config(config, "s3accessExterno", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config(config, "s3accessExterno", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    prm_aws_access_key_id = pl.validar_parametros(
        cl.valor_config(config, "s3accessExterno", "aws_access_key_id"),
        "El parametro access_key_id es obligatorio."
    )
    prm_aws_secret_access_key = pl.validar_parametros(
        cl.valor_config(config, "s3accessExterno", "aws_secret_access_key"),
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
    print("Cargando dataset de zona input")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "input"),
            "la ruta remota para la data de input es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "input"),
            "la ruta local para la data de input es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "input"),
            "el nombre del dataset de entrenamiento es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    nombre_archivo = lee_s3(config, nombre_local, nombre_remoto)
    df_ad = pd.read_csv(nombre_archivo)
    return df_ad


def guardar_dataset(df_ad, config):
    print("Guardando salida")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "raw"),
            "la ruta remota para la data de input es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "raw"),
            "la ruta local para la data de input es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "raw"),
            "el nombre del dataset de entrenamiento es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    df_ad.to_csv(nombre_local, index=False)
    escribe_s3(config, nombre_local, nombre_remoto)


def inicio():
    # get config info
    config = cl.leer_config(".", "config")

    # get dataset
    df_ad = carga_dataset(config)
    # save dataset
    guardar_dataset(df_ad, config)


if __name__ == "__main__":
    inicio()
