from os import path
import pandas as pd
import s3 as s3
import files as f1


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
