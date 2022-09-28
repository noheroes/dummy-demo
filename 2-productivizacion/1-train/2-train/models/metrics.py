import json
from kfp.components import OutputPath, create_component_from_func
from os import path

import libs.config_lib as cl
import libs.params_lib as pl

metrics = {}


def create_metrics(
    train_mse,
    train_rmse,
    train_r2,
    train_mape,
    test_mse,
    test_rmse,
    test_r2,
    test_mape,
    average_house_price
):
    return {
        "metrics": [
            {
                "name": "train_mse",
                "numberValue": train_mse,
                "format": "RAW"
            },
            {
                "name": "train_rmse",
                "numberValue": train_rmse,
                "format": "RAW"
            },
            {
                "name": "train_r2",
                "numberValue": train_r2,
                "format": "RAW"
            },
            {
                "name": "train_mape",
                "numberValue": train_mape,
                "format": "RAW"
            },
            {
                "name": "average_house_price",
                "numberValue": average_house_price,
                "format": "RAW"
            }
        ]
    }


def save_metrics(metrics):
    config = cl.leer_config("..", "config")
    nombre_archivo = path.join(
        pl.validar_parametros(
            cl.valor_config(config, "paths", "metrics"),
            "la ruta para la metricas es obligatoria."),
        pl.validar_parametros(
            cl.valor_config(config, "files", "metrics"),
            "el nombre del archivo de metricas es obligatorio.")
    )
    with open(nombre_archivo, 'w') as f:
        json.dump(metrics, f)


def produce_metrics(mlpipeline_metrics_path: OutputPath("Metrics")):
    metrics = get_metrics()
    with open(mlpipeline_metrics_path, 'w') as f:
        json.dump(metrics, f)


def get_metrics(self):
    return self.metrics


def metadata(metadata):
    with open('./mlpipeline-ui-metadata.json', 'w') as m:
        json.dump(metadata, m)


def create_component():
    return create_component_from_func(
        produce_metrics,
        base_image='python:3.7',
        packages_to_install=[],
        output_component_file='./component.yaml')
