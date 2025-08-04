import subprocess
import os
import platform
import sys

def install_python_requirements(req_path):
    with open(req_path, 'r') as f:
        for line in f:
            package = line.strip()
            if package and not package.startswith('#'):
                print(f"Instalando paquete Python: {package}")
                subprocess.run(['pip', 'install', package], check=True)

def install_node_modules(mod_path, node_dir):
    with open(mod_path, 'r') as f:
        for line in f:
            module = line.strip()
            if module and not module.startswith('#'):
                print(f"Instalando módulo Node.js: {module} en {node_dir}")
                subprocess.run(['npm', 'install', module], cwd=node_dir, check=True)

def is_chocolatey_installed():
    try:
        result = subprocess.run(['choco', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_chocolatey():
    print("Chocolatey no está instalado. Instalando Chocolatey...")
    try:
        powershell_command = (
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; "
            "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        )
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", powershell_command], check=True)
        print("Chocolatey instalado correctamente.")
    except subprocess.CalledProcessError:
        print("Error al instalar Chocolatey. Por favor instala Chocolatey manualmente desde https://chocolatey.org/install")
        sys.exit(1)

def install_nmap():
    system = platform.system()
    print(f"Detectando sistema operativo: {system}")
    try:
        if system == "Linux":
            print("Instalando nmap para Linux usando apt-get...")
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nmap'], check=True)

        elif system == "Windows":
            if not is_chocolatey_installed():
                install_chocolatey()
            print("Instalando nmap usando Chocolatey...")
            subprocess.run(['choco', 'install', 'nmap', '-y'], check=True)

        else:
            print(f"Sistema operativo {system} no soportado para instalación automática de nmap.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar nmap: {e}")

if __name__ == '__main__':
    req_file = 'dependencies/requirements.txt'
    mod_file = 'dependencies/modulos.txt'
    node_directory = 'stelarys/JS'

    if not os.path.exists(req_file):
        print(f"No se encontró el archivo {req_file}")
    else:
        install_python_requirements(req_file)

    if not os.path.exists(mod_file):
        print(f"No se encontró el archivo {mod_file}")
    else:
        install_node_modules(mod_file, node_directory)

    install_nmap()
