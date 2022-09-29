import libs.params_lib as pl
import libs.files_lib as fl


def leer_config(config_path, config_name):
    config_name = pl.validar_parametros(
        config_name,
        'El nombre del archivo de configuración es obligatorio.')
    ruta_parametros = f"{config_path}/config/{config_name}.json"
    return fl.leer_json(ruta_parametros)


def valor_config(config, param1, param2="", param3=""):
    valor = fl.valor_json(config, param1, param2, param3) 
    return valor
