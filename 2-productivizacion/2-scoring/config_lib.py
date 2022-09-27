import params_lib as pl
import files_lib as fl


def leer_config(path, config_name):
    config_name = pl.validar_parametros(
        config_name,
        'El nombre del archivo de configuración es obligatorio.')
    ruta_parametros = f"{path}/config/{config_name}.json"
    return fl.leer_json(ruta_parametros)


def valor_config(config, param1, param2, param3=''):
    return fl.valor_json(config, param1, param2, param3)
