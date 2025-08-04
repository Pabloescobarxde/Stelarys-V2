from stelarys.src.utiles.imports import *

def get_system_info():
    system = platform.system()
    if system == "Windows":
        return f"Windows {platform.release()}"
    elif system == "Linux":
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                name = None
                version = None
                for line in lines:
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=')[1].strip().strip('"')
                    elif line.startswith('NAME='):
                        name = line.split('=')[1].strip().strip('"')
                    elif line.startswith('VERSION='):
                        version = line.split('=')[1].strip().strip('"')
                if name and version:
                    return f"{name} {version}"
                elif name:
                    return name
        except:
            pass
        return f"Linux {platform.release()}"
    elif system == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    else:
        return f"{system} {platform.release()}"