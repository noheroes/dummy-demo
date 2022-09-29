from os import path
import libs.files as f1
import libs.s3 as s3
import libs.files_lib as fl

def leer_algoritmo_selected(config):
    remotepath = f1.obtener_ruta(config, "s3paths", "algoritmo_selected",
            "la ruta remota para el algoritmo selected es obligatoria.")
    localpath = f1.obtener_ruta(config, "paths", "algoritmo_selected",
            "la ruta local para el algoritmo selected es obligatoria.")
    algoritmo_selected = f1.obtener_ruta(config, "files", "algoritmo_selected",
            "el nombre del archivo del algoritmo selected es obligatorio")
    nombre_local = path.join(localpath, algoritmo_selected)
    nombre_remoto = path.join(remotepath, algoritmo_selected)
    nombre_archivo = s3.lee_s3(config, nombre_local, nombre_remoto)    

    info = fl.leer_json(nombre_archivo)
    algoritmo_selected = fl.valor_json(info, "algoritmo_selected")
    return algoritmo_selected