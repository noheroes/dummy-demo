from os import path
import json

# utils
import s3_lib as s3l
import config_lib as cl
import params_lib as pl


def crea_manifiesto_modelo(config, nombre_modelo, version_modelo):
    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    models_path = pl.validar_parametros(
        cl.valor_config(config, "s3paths", "models" ),
        "La ruta de los modelo no puede ser nula"
    )
    ruta_manifiesto = pl.validar_parametros(
        cl.valor_config(config, "paths", "nombre"),
        "El nombre del manifiesto es obligatorio"
    )
    nombre_manifiesto = pl.validar_parametros(
        cl.valor_config(config, "manifiesto", "nombre"),
        "El nombre del manifiesto es obligatorio"
    )

    manifiesto = {
        "name": nombre_modelo,
        "implementation": "model.ServingModel",
        "parameters": {
            "uri": path.join(prm_aws_endpoint,
                             prm_aws_s3_bucket,
                             models_path,
                             nombre_modelo),
            "version": version_modelo
        }
    }
    with open(path.join(ruta_manifiesto, nombre_manifiesto), "w") as f:
        json.dump(manifiesto, f)


def escribe_s3(config, localpath, referencepath):
    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config("s3access", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    prm_aws_access_key_id = pl.validar_parametros(
        cl.valor_config("s3access", "aws_access_key_id"),
        "El parametro access_key_id es obligatorio."
    )
    prm_aws_secret_access_key = pl.validar_parametros(
        cl.valor_config("s3access", "aws_secret_access_key"),
        "El parametro secret_access_key es obligatorio."
    )
    s3l.uploadS3(prm_aws_endpoint,
                 prm_aws_access_key_id,
                 prm_aws_secret_access_key,
                 prm_aws_s3_bucket,
                 localpath,
                 referencepath)


def escribe_modelo(config, algoritmo_selected, ruta_modelos, archivo_modelo):
    ruta_archivo = pl.validar_parametros(
        cl.valor_config(config, "paths", "models"),
        "La ruta del archivo de modelo es obligatorio."
    )
    nombre_local = path.join(ruta_archivo, archivo_modelo)
    nombre_remoto = path.join(ruta_modelos, algoritmo_selected, archivo_modelo)
    escribe_s3(config, nombre_local, nombre_remoto)


def escribe_hiperparametros(config, algoritmo_selected, s3ruta_modelos):
    ruta_archivo = pl.validar_parametros(
        cl.valor_config(config, "paths", "hyperparameters"),
        "La ruta del archivo de hiperparametros es obligatorio."
    )
    nombre_archivo = pl.validar_parametros(
        cl.valor_config(config, "models", algoritmo_selected, "hyperparameters"),
        "El nombre del archivo de hiperparametros es obligatorio."
    )
    nombre_local = path.join(ruta_archivo, nombre_archivo)
    nombre_remoto = path.join(s3ruta_modelos, algoritmo_selected, nombre_archivo)
    escribe_s3(config, nombre_local, nombre_remoto)


def escribe_features(config, algoritmo_selected, s3ruta_modelos):
    ruta_archivo = pl.validar_parametros(
        cl.valor_config(config, "paths", "features"),
        "La ruta del archivo de features es obligatorio."
    )
    nombre_archivo = pl.validar_parametros(
        cl.valor_config(config, "files", "features"),
        "El nombre del archivo de features es obligatorio."
    )
    nombre_local = path.join(ruta_archivo, nombre_archivo)
    nombre_remoto = path.join(s3ruta_modelos, algoritmo_selected, nombre_archivo)
    escribe_s3(config, nombre_local, nombre_remoto)


def escribe_dataset(config, algoritmo_selected, s3ruta_modelos, tipo_dataset, nombre_dataset):
    ruta_archivo = pl.validar_parametros(
        cl.valor_config(config, "paths", tipo_dataset),
        "La ruta del archivo de features es obligatorio."
    )
    nombre_local = path.join(ruta_archivo, nombre_dataset)
    nombre_remoto = path.join(s3ruta_modelos, algoritmo_selected, nombre_dataset)
    escribe_s3(config, nombre_local, nombre_remoto)


def escribe_metrics(config, algoritmo_selected, s3ruta_modelos):
    ruta_archivo = pl.validar_parametros(
        cl.valor_config(config, "paths", "metrics"),
        "La ruta del archivo de metricas es obligatorio."
    )
    nombre_archivo = pl.validar_parametros(
        cl.valor_config(config, "files", "metrics"),
        "El nombre del archivo de metricas es obligatorio."
    )
    nombre_local = path.join(ruta_archivo, nombre_archivo)
    nombre_remoto = path.join(s3ruta_modelos, algoritmo_selected, nombre_archivo)
    escribe_s3(config, nombre_local, nombre_remoto)


def main(algoritmo_selected, archivo_modelo, hiperparametros, features, metrics):
    config = cl.leer_config("..", "config")
    s3models_path = pl.validar_parametros(
        cl.valor_config(config, "s3paths", "models"),
        "La ruta de los modelos es obligatoria"
    )
    train_name = pl.validar_parametros(
        cl.valor_config(config, "files", "train"),
        "El nombre del archivo de entrenamiento es obligatorio."
    )
    test_name = pl.validar_parametros(
        cl.valor_config(config, "files", "test"),
        "El nombre del archivo de entrenamiento es obligatorio."
    )

    escribe_modelo(config, algoritmo_selected, s3models_path, archivo_modelo)
    escribe_hiperparametros(config, algoritmo_selected, s3models_path)
    escribe_features(config, algoritmo_selected, s3models_path)
    escribe_dataset(config, algoritmo_selected, s3models_path, 'train', train_name)
    escribe_dataset(config, algoritmo_selected, s3models_path, 'test', test_name)
    escribe_metrics(config, algoritmo_selected, s3models_path)


