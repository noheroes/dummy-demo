import requests
import json
from os import path
import config_lib as cl
import s3_lib as s3l
import params_lib as pl
import io


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


def guardar_log(jsonLog, config):
    print("Guardando log")
    remotepath = pl.validar_parametros(
            cl.valor_config(config, "s3paths", "log"),
            "la ruta remota para la data de analytic es obligatoria.")
    localpath = pl.validar_parametros(
            cl.valor_config(config, "paths", "log"),
            "la ruta local para la data de analytic es obligatoria.")
    archivo = pl.validar_parametros(
            cl.valor_config(config, "files", "log"),
            "el nombre del dataset de entrenamiento es obligatorio")
    nombre_local = path.join(localpath, archivo)
    nombre_remoto = path.join(remotepath, archivo)
    with io.open(nombre_local, 'w', encoding='utf8') as outfile:
        str_ = json.dumps(jsonLog,
                          indent=4,
                          sort_keys=True,
                          separators=(',', ': '),
                          ensure_ascii=False)
        outfile.write(str_)
    escribe_s3(config, nombre_local, nombre_remoto)


def get_enpoint(config):
    endpoint_url = pl.validar_parametros(
        cl.valor_config(config, "endpoint", "url"),
        "La url del endpoint es obligatorio."
    )
    endpoint_parameter = pl.validar_parametros(
        cl.valor_config(config, "endpoint", "modelParameter"),
        "El parametro de url del endpoint es obligatorio."
    )
    modelVersion = pl.validar_parametros(
        cl.valor_config(config, "endpoint", "version"),
        "El parametro de url del endpoint es obligatorio."
    )
    endpoint = "".join([endpoint_url, endpoint_parameter])
    endpoint = endpoint.format(modelVersion=modelVersion)
    return endpoint


def scoring(config):
    url = get_enpoint(config)
    print(url)
    param = json.dumps([{"x": "1"}])
    inference_request = {
        "inputs": [
            {
                "name": "rep_data",
                "shape": [len(param)],
                "datatype": "FP32",
                "data": param
                }
            ]
        }
    try:
        response = requests.post(url, json=inference_request).json()
        modelName = response["model_name"]
        modelVersion = response["model_version"]
        predictionPath = response["outputs"][0]["data"][0]["prediction_path"]
        log = {
                "model_name": modelName,
                "model_version": modelVersion,
                "prediction_path": predictionPath
               }
    except Exception as e:
        print(e)
        raise(e)

    return log


def inicio():
    try:
        # get config info
        config = cl.leer_config(".", "config")

        # endpoint scoring
        log = scoring(config)

        guardar_log(log, config)
    except Exception as e:
        print(f'error: {e}')


if __name__ == "__main__":
    inicio()
