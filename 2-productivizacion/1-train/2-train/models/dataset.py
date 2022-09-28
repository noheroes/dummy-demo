from os import path
import pandas as pd
import libs.s3 as s3
import libs.files as f1


def read_prepare_dataset(config, target):
    # to visualise al the columns in the dataframe
    pd.pandas.set_option('display.max_columns', None)

    remotepath = f1.obtener_ruta(config, "s3paths", "dataset",
            "la ruta remota para la data de entrenamiento es obligatoria.")
    localpath = f1.obtener_ruta(config, "paths", "train",
            "la ruta local para la data de entrenamiento es obligatoria.")
    archivo_train = f1.obtener_ruta(config, "files", "train",
            "el nombre del dataset de entrenamiento es obligatorio")
    nombre_local = path.join(localpath, archivo_train)
    nombre_remoto = path.join(remotepath, archivo_train)
    nombre_archivo = s3.lee_s3(config, nombre_local, nombre_remoto)
    X_train = pd.read_csv(nombre_archivo)

    remotepath = f1.obtener_ruta(config, "s3paths", "dataset",
            "la ruta remota para la data de test es obligatoria.")
    localpath = f1.obtener_ruta(config, "paths", "test",
            "la ruta local para la data de test es obligatoria.")
    archivo_test = f1.obtener_ruta(config, "files", "test",
            "el nombre del dataset de test es obligatorio")
    nombre_local = path.join(localpath, archivo_test)
    nombre_remoto = path.join(remotepath, archivo_test)
    nombre_archivo = s3.lee_s3(config, nombre_local, nombre_remoto)
    X_test = pd.read_csv(nombre_archivo)

    X_train.head()
    y_train = X_train[target]
    y_test = X_test[target]
    return X_train, y_train, X_test, y_test