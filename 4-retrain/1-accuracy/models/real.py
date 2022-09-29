from os import path
import pandas as pd
import libs.files as f1
import libs.s3 as s3
import libs.files_lib as fl


def leer_real(config):
    remotepath = f1.obtener_ruta(config, "s3paths", "real",
            "la ruta remota para el real es obligatoria.")
    localpath = f1.obtener_ruta(config, "paths", "real",
            "la ruta local para el real es obligatoria.")
    real = f1.obtener_ruta(config, "files", "real",
            "el nombre del archivo del real es obligatorio")
    nombre_local = path.join(localpath, real)
    nombre_remoto = path.join(remotepath, real)
    nombre_archivo = s3.lee_s3(config, nombre_local, nombre_remoto)    

    real = pd.read_csv(nombre_archivo, index_col=None)
    return real