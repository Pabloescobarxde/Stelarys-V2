from stelarys.src.utiles.imports import *


def get_version(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except:
        return None

def is_admin():
   
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

def run_command(command, shell=True):
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_python():
    sistema = platform.system().lower()
    print(f"\n     {GRAY}({G}→{GRAY}) {W}Instalando Python...{N}")
    
    if sistema == "linux":
        # Ubuntu/Debian
        commands = [
            "sudo apt update",
            "sudo apt install -y python3 python3-pip python3-venv"
        ]
        for cmd in commands:
            print(f" {GRAY}Ejecutando: {cmd}{N}")
            success, stdout, stderr = run_command(cmd)
            if not success:
                print(f" {R}Error: {stderr}{N}")
                return False
        return True
    
    elif sistema == "windows":
        print(f"     {YELLOW}Para Windows, descarga Python desde: https://python.org/downloads{N}")
        print(f"     {YELLOW}O usa winget: winget install Python.Python.3{N}")
    
        if shutil.which("winget"):
            success, stdout, stderr = run_command("winget install Python.Python.3")
            return success
        return False
    
    return False

def install_nodejs():
   
    sistema = platform.system().lower()
    print(f"\n     {GRAY}({G}→{GRAY}) {W}Instalando Node.js...{N}")
    
    if sistema == "linux":
     
        commands = [
            "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -",
            "sudo apt-get install -y nodejs"
        ]
        for cmd in commands:
            print(f" {GRAY}Ejecutando: {cmd}{N}")
            success, stdout, stderr = run_command(cmd)
            if not success:
                print(f" {R}Error: {stderr}{N}")
                # Fallback: usar snap
                print(f" {YELLOW}Intentando con snap...{N}")
                success, stdout, stderr = run_command("sudo snap install node --classic")
                return success
        return True
    
    elif sistema == "windows":
        print(f"     {YELLOW}Para Windows, descarga Node.js desde: https://nodejs.org{N}")
        print(f"     {YELLOW}O usa winget: winget install OpenJS.NodeJS{N}")
        if shutil.which("winget"):
            success, stdout, stderr = run_command("winget install OpenJS.NodeJS")
            return success
        return False
    
    return False

def install_git():
    
    sistema = platform.system().lower()
    print(f"\n {GRAY}({G}→{GRAY}) {W}Instalando Git...{N}")
    
    if sistema == "linux":
        success, stdout, stderr = run_command("sudo apt install -y git")
        if success:
            print(f"     {G}Git instalado correctamente{N}")
        else:
            print(f"     {R}Error instalando Git: {stderr}{N}")
        return success
    
    elif sistema == "windows":
        print(f"     {YELLOW}Para Windows, descarga Git desde: https://git-scm.com{N}")
        print(f"     {YELLOW}O usa winget: winget install Git.Git{N}")
        if shutil.which("winget"):
            success, stdout, stderr = run_command("winget install Git.Git")
            return success
        return False
    
    return False

def check_and_install_dependencies(auto_install=True):
    sistema = get_system_info()
    arquitectura = platform.machine()
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    print(f"     {GRAY}({G}*{GRAY}) {W}Información del Sistema{N}")
    print(f"      {R}- {W}Sistema Operativo: {C}{sistema}{N}")
    print(f"      {R}- {W}Arquitectura: {C}{arquitectura}{N}")
    print(f"      {R}- {W}Python Actual: {C}v{python_version}{N}\n")
    
    
    missing_dependencies = []
    
   
    print(f"     {GRAY}({G}*{GRAY}) {W}Estado de Dependencias{N}")
    
    # Python
    python_instalado = shutil.which("python") or shutil.which("python3")
    if python_instalado:
        python_cmd = "python --version" if shutil.which("python") else "python3 --version"
        python_ver = get_version(python_cmd)
        if python_ver:
            python_ver = python_ver.replace("Python ", "v")
        estado_python = f"{G}✓ Instalado{N}"
        version_python = f"{C}{python_ver}{N}" if python_ver else f"{YELLOW}Versión no detectada{N}"
    else:
        estado_python = f"{R}✗ No encontrado{N}"
        version_python = f"{R}No disponible{N}"
        missing_dependencies.append("python")
    
    print(f"      {R}- {W}Python: {estado_python} {version_python}")
    
    # Node.js
    node_instalado = shutil.which("node") or shutil.which("nodejs")
    if node_instalado:
        node_ver = get_version("node --version")
        estado_node = f"{G}✓ Instalado{N}"
        version_node = f"{C}{node_ver}{N}" if node_ver else f"{YELLOW}Versión no detectada{N}"
    else:
        estado_node = f"{R}✗ No encontrado{N}"
        version_node = f"{R}No disponible{N}"
        missing_dependencies.append("nodejs")
    
    print(f"      {R}- {W}Node.js: {estado_node} {version_node}")
    
    # NPM
    if node_instalado:
        npm_instalado = shutil.which("npm")
        if npm_instalado:
            npm_ver = get_version("npm --version")
            estado_npm = f"{G}✓ Instalado{N}"
            version_npm = f"{C}v{npm_ver}{N}" if npm_ver else f"{YELLOW}Versión no detectada{N}"
        else:
            estado_npm = f"{R}✗ No encontrado{N}"
            version_npm = f"{R}No disponible{N}"
        print(f"      {R}- {W}NPM: {estado_npm} {version_npm}")
    
    # Git
    git_instalado = shutil.which("git")
    if git_instalado:
        git_ver = get_version("git --version")
        if git_ver:
            git_ver = git_ver.replace("git version ", "v")
        estado_git = f"{G}✓ Instalado{N}"
        version_git = f"{C}{git_ver}{N}" if git_ver else f"{YELLOW}Versión no detectada{N}"
    else:
        estado_git = f"{R}✗ No encontrado{N}"
        version_git = f"{R}No disponible{N}"
        missing_dependencies.append("git")
    
    print(f"      {R}- {W}Git: {estado_git} {version_git}")
    
   
    if missing_dependencies and auto_install:
        print(f"\n {GRAY}({G}!{GRAY}) {W}Dependencias faltantes detectadas: {R}{', '.join(missing_dependencies)}{N}")
        
        
        if platform.system().lower() == "linux" and not is_admin():
            print(f" {YELLOW}Nota: Se requieren permisos de sudo para instalar dependencias{N}")
        
        respuesta = input(f"\n {GRAY}({G}?{GRAY}) {W}¿Deseas instalar las dependencias faltantes automáticamente? (s/n): {N}").lower()
        
        if respuesta in ['s', 'si', 'y', 'yes']:
            installation_success = True
            
           
            if "python" in missing_dependencies:
                if not install_python():
                    installation_success = False
            
            if "nodejs" in missing_dependencies:
                if not install_nodejs():
                    installation_success = False
            
            if "git" in missing_dependencies:
                if not install_git():
                    installation_success = False
            
            if installation_success:
                print(f"\n {GRAY}({G}✓{GRAY}) {W}Instalación completada. Reinicia tu terminal para aplicar los cambios.{N}")
            
                return check_and_install_dependencies(auto_install=False)
            else:
                print(f"\n {GRAY}({R}✗{GRAY}) {W}Algunas instalaciones fallaron. Verifica manualmente.{N}")
                return False
        else:
            print(f"\n     {GRAY}({G}i{GRAY}) {W}Instalación manual requerida{N}")
            print(f"      {R}- {W}Python: {C}https://python.org/downloads{N}")
            print(f"      {R}- {W}Node.js: {C}https://nodejs.org{N}")
            print(f"      {R}- {W}Git: {C}https://git-scm.com{N}")
            return False
    
   
    dependencias_ok = len(missing_dependencies) == 0
    if dependencias_ok:
        print(f"\n     {GRAY}({G}✓{GRAY}) {W}Todas las dependencias principales están instaladas{N}")
        return True
    else:
        print(f"\n     {GRAY}({R}✗{GRAY}) {W}Faltan dependencias críticas: {R}{', '.join(missing_dependencies)}{N}")
        return False

def check_dependencies():
    return check_and_install_dependencies(auto_install=True)