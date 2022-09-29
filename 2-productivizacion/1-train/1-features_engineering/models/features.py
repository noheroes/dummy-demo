from os import path
import pandas as pd
import libs.s3 as s3
import libs.files as f1


def read_selected_features(config, additional_feature=''):
    file = 'features'
    remotepath = f1.obtener_ruta(config, "s3paths", file,
            "la ruta remota para los features es obligatoria.")
    localpath = f1.obtener_ruta(config, "paths", file,
            "la ruta local para los features es obligatoria.")
    archivo_test = f1.obtener_ruta(config, "files", file,
            "el nombre del archivo de features es obligatorio")
    nombre_local = path.join(localpath, archivo_test)
    nombre_remoto = path.join(remotepath, archivo_test)
    nombre_archivo = s3.lee_s3(config, nombre_local, nombre_remoto)
    features = pd.read_csv(nombre_archivo)

    features = features['0'].to_list()
    if additional_feature != '':
        features = features + [additional_feature]

    return features


def write_selected_features(config, selected_features):
    file = 'features'
    remotepath = f1.obtener_ruta(config, "s3paths", file,
            "la ruta remota para los features es obligatoria.")
    localpath = f1.obtener_ruta(config, "paths", file,
            "la ruta local para los features es obligatoria.")
    archivo_test = f1.obtener_ruta(config, "files", file,
            "el nombre del archivo de features es obligatorio")
    nombre_local = path.join(localpath, archivo_test)
    nombre_remoto = path.join(remotepath, archivo_test)
    selected_features.to_csv(nombre_local, index=False)
    s3.escribe_s3(config, nombre_local, nombre_remoto)