from stelarys.src.utiles.imports import *


def obtener_versiones():
    # Python version
    try:
        python_version = sys.version.split()[0]
    except:
        python_version = f"{R}OFF ({W}https://www.python.org/downloads/{R})"

    # NodeJS version
    try:
        node_version = os.popen("node -v").read().strip()
        if not node_version:
            raise Exception()
    except:
        node_version = f"{R}OFF ({W}https://nodejs.org/en/download/{R})"

    return python_version, node_version