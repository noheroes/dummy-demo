import libs.config_lib as cl
import libs.params_lib as pl
import libs.files_lib as fl


def obtener_ruta(config, raiz, ruta, mensaje):
    return pl.validar_parametros(
            cl.valor_config(config, raiz, ruta),
            mensaje)


def obtener_ruta2(config, raiz, raiz2, ruta, mensaje):
    return pl.validar_parametros(
            cl.valor_config(config, raiz, raiz2, ruta),
            mensaje)


def leer_json(ruta_archivo):
    return fl.leer_json(ruta_archivo)


def guardar_json(ruta_archivo, data_json):
    return fl.guardar_json(ruta_archivo, data_json)