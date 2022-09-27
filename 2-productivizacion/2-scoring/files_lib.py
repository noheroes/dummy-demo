import os
import json
import fnmatch
import params_lib as pl


def leer_json(ruta_archivo):
    ruta_archivo = pl.validar_parametros(
        ruta_archivo,
        'La ruta del archivo es obligatoria.')

    with open(ruta_archivo) as f:
        try:
            archivo = json.load(f)
        except IOError as e:
            e = ("El archivo de json no puede ser leido.")
            raise Exception(e)
    return archivo


def valor_json(config, param1, param2="", param3=""):
    config = pl.validar_parametros(config, "El contenido del archivo es obligatorio.")
    param1 = pl.validar_parametros(param1, "El parámetro 1 es obligatorio.")

    try:
        if param3 != "":
            valor = config[param1][param2][param3]
        if param2 != "":
            valor = config[param1][param2]
        else:
            valor = config[param1]
    except Exception as e:
        e = ("El argumento no es el correcto")
        raise Exception(e)
    return valor


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

