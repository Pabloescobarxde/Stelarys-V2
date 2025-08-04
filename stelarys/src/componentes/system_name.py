from stelarys.src.utiles.imports import *

def obtener_nombre_pc():
    try:
        return os.uname().nodename
    except AttributeError:
        return os.getenv("COMPUTERNAME", "localhost")

nombre_pc = obtener_nombre_pc()