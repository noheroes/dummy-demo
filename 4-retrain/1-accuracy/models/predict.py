from os import path
import pandas as pd
import libs.files as f1
import libs.s3 as s3
import libs.files_lib as fl


def leer_predict(config):
    remotepath = f1.obtener_ruta(config, "s3paths", "predict",
            "la ruta remota para el predict es obligatoria.")
    localpath = f1.obtener_ruta(config, "paths", "predict",
            "la ruta local para el predict es obligatoria.")
    predict = f1.obtener_ruta(config, "files", "predict",
            "el nombre del archivo del predict es obligatorio")
    nombre_local = path.join(localpath, predict)
    nombre_remoto = path.join(remotepath, predict)
    nombre_archivo = s3.lee_s3(config, nombre_local, nombre_remoto)    

    predict = pd.read_csv(nombre_archivo, index_col=None)
    return predict