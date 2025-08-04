from stelarys.src.utiles.imports import *

def get_appdata_path(*paths):
    if sys.platform == 'win32':
        base_dir = os.getenv('APPDATA')
        if base_dir is None:
            raise EnvironmentError("La variable de entorno APPDATA no está definida en Windows.")
    else:
        base_dir = os.path.expanduser('~/.config')
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, *paths)