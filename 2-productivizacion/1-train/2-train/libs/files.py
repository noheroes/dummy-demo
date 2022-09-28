import libs.config_lib as cl
import libs.params_lib as pl


def obtener_ruta(config, raiz, ruta, mensaje):
    return pl.validar_parametros(
            cl.valor_config(config, raiz, ruta),
            mensaje)


def obtener_ruta2(config, raiz, raiz2, ruta, mensaje):
    return pl.validar_parametros(
            cl.valor_config(config, raiz, raiz2, ruta),
            mensaje)

