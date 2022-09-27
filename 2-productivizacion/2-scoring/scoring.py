# Import libraries
import os
from os import path

import pandas as pd
import gc
import joblib

import s3_lib as s3l
import config_lib as cl
import params_lib as pl


def carga_dataset(parametrosScoring, periodo):
    print("Cargando dataset de zona raw")
    rutaArchivo = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_Analytic_Data"),
        "La ruta raw del archivo de parametros no puede ser nula"
    )
    extensionArchivo = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "ExtCSV"),
        "La ruta raw del archivo de parametros no puede ser nula"
    )
    nombreSalida = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_Analytic_Data"),
        "La ruta raw del archivo de parametros no puede ser nula"
    )
    rutaArchivoPreparada = path.join(rutaArchivo, periodo)

    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    prm_aws_access_key_id = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_access_key_id"),
        "El parametro access_key_id es obligatorio."
    )
    prm_aws_secret_access_key = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_secret_access_key"),
        "El parametro secret_access_key es obligatorio."
    )
    nombreArchivo = "".join([nombreSalida, periodo, extensionArchivo])
    files = path.join(rutaArchivoPreparada, nombreArchivo)

    if not files.endswith(extensionArchivo):
        raise Exception(
            f"No se encontraron archivos {extensionArchivo} en la ruta: \
            {rutaArchivoPreparada} del bucket {prm_aws_s3_bucket}")

    archivo = s3l.readS3(prm_aws_endpoint,
                         prm_aws_access_key_id,
                         prm_aws_secret_access_key,
                         prm_aws_s3_bucket,
                         files)
    df_ad = pd.read_csv(archivo)
    return df_ad


def carga_modelo(parametrosScoring):
    print("Cargando modelo de bucket")
    nombreModelo = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_Model"),
        "El nombre del modelo no puede ser nulo"
    )
    rutaModelo = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_Model"),
        "La ruta del modelo no puede ser nula"
    )
    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    prm_aws_access_key_id = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_access_key_id"),
        "El parametro access_key_id es obligatorio."
    )
    prm_aws_secret_access_key = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_secret_access_key"),
        "El parametro secret_access_key es obligatorio."
    )
    modelo_remoto = ''.join([rutaModelo, nombreModelo])

    nombreModelo = s3l.readS3(prm_aws_endpoint,
                              prm_aws_access_key_id,
                              prm_aws_secret_access_key,
                              prm_aws_s3_bucket,
                              modelo_remoto)
    return nombreModelo


def carga_features(parametrosScoring):
    print("Leyendo Features")
    nombreFeatures = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_Features"),
        "El nombre de las features no puede ser nulo"
    )
    rutaFeatures = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_Features"),
        "La ruta de las features no puede ser nula"
    )
    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_configvalor(parametrosScoring, "s3access", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    prm_aws_access_key_id = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_access_key_id"),
        "El parametro access_key_id es obligatorio."
    )
    prm_aws_secret_access_key = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_secret_access_key"),
        "El parametro secret_access_key es obligatorio."
    )
    features_remoto = ''.join([rutaFeatures, nombreFeatures])

    nombreFeatures = s3l.readS3(prm_aws_endpoint,
                                prm_aws_access_key_id,
                                prm_aws_secret_access_key,
                                prm_aws_s3_bucket,
                                features_remoto)
    return nombreFeatures


def scoring(df_ad, features, modelo):
    print("Ejecutando Scoring")

    # Load model
    model = joblib.load(modelo)

    # Execute model
    predict = pd.DataFrame(model.predict(df_ad[features],
                                         num_iteration=model.best_iteration))
    gc.collect()

    return predict


def guardar_salida(predict, parametrosScoring) -> str:
    print("Guardando salida")
    nombreSalida = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "name", "Name_PredictTemp_Data"),
        "El nombre del archivo de salida no puede ser nulo"
    )
    rutaSalida = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "Ruta_PredictTemp_Data"),
        "La ruta del archivo de salida no puede ser nula"
    )
    extensionArchivo = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "paths", "ExtCSV"),
        "La extension del archivo de salida no puede ser nula"
    )
    salida = ''.join([nombreSalida, extensionArchivo])
    nombreSalida = path.join(rutaSalida, salida)

    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    prm_aws_access_key_id = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_access_key_id"),
        "El parametro access_key_id es obligatorio."
    )
    prm_aws_secret_access_key = pl.validar_parametros(
        cl.valor_config(parametrosScoring, "s3access", "aws_secret_access_key"),
        "El parametro secret_access_key es obligatorio."
    )

    response = s3l.writeS3(prm_aws_endpoint,
                           prm_aws_access_key_id,
                           prm_aws_secret_access_key,
                           prm_aws_s3_bucket,
                           nombreSalida,
                           predict)

    print(f'response: {response}')
    return nombreSalida


def inicio():
    # get config info
    algoritmo = os.getenv("ALGORITMO")
    archivo_config = f"config_{algoritmo}"
    parametrosScoring = cl.leer_config(archivo_config)
    # get dataset
    df_ad = carga_dataset(parametrosScoring)
    # get features
    features = carga_features(parametrosScoring)
    # get model
    nombreModelo = carga_modelo(parametrosScoring)
    # execute model
    df_predict = scoring(df_ad, features, nombreModelo)
    # save predict
    nombre_salida = guardar_salida(df_predict, parametrosScoring)
    return nombre_salida


if __name__ == "__main__":
    inicio()