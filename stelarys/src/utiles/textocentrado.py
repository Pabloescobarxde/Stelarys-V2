from stelarys.src.utiles.imports import *


def centrar_texto(texto):
    terminal_ancho = shutil.get_terminal_size().columns
    for linea in texto.split('\n'):
        print(" " * ((terminal_ancho - len(linea)) // 2) + linea)