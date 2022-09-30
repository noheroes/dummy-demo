import json
from kfp.components import OutputPath, create_component_from_func
from os import path

import libs.s3 as s3
import libs.files as f1

metrics = {}


def create_metrics(
    accuracy
):
    accuracy = json.loads(accuracy)
    return json.dumps({
        "accuracy": [
            {
                "id": accuracy["accion"],
                "descripcion": accuracy["descripcion"],
                "format": "RAW"
            }
        ]
    })


def save_metrics(config, metrics):
    nombre_archivo = path.join(
        f1.obtener_ruta(config, "paths", "metrics",
           "la ruta para la metricas es obligatoria."),
        f1.obtener_ruta(config, "files", "metrics",
           "el nombre del archivo de metricas es obligatorio.")
    )
    f1.guardar_json(nombre_archivo, metrics)


def read_metrics(config, algoritmo_selected):
    remotepath = f1.obtener_ruta(config, "s3paths", "metrics",
            "la ruta remota para las metricas es obligatoria.")
    localpath = f1.obtener_ruta(config, "paths", "metrics",
            "la ruta local para las metricas es obligatoria.")
    metrics = f1.obtener_ruta(config, "files", "metrics",
            "el nombre del archivo de metricas es obligatorio")
    nombre_local = path.join(localpath, metrics)
    nombre_remoto = path.join(remotepath, algoritmo_selected, metrics)
    nombre_archivo = s3.lee_s3(config, nombre_local, nombre_remoto)
    return f1.leer_json(nombre_archivo)