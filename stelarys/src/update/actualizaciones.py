from stelarys.src.utiles.imports import *

class GitHubUpdater:
    def __init__(self, repo_owner="Pabloescobarxde", repo_name="Stelarys-V2", current_version="2.0.0"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.sistema = platform.system().lower()
        
    def get_latest_release(self):
        try:
            print("")
            print(f"     {GRAY}({G}→{GRAY}) {W}Verificando actualizaciones en GitHub...{N}")
            
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Stelarys-Updater'
            }
            
            response = requests.get(self.github_api_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            return release_data
            
        except requests.exceptions.RequestException as e:
            print(f"     {R}Error conectando con GitHub: {str(e)}{N}")
            return None
        except json.JSONDecodeError:
            print(f"     {R}Error procesando respuesta de GitHub{N}")
            return None
    
    def parse_version(self, version_string):
        clean_version = version_string.lower()
        prefixes = ['v', 'version', 'stelarys', 'stelarys-v', 'stelarys v']
        
        for prefix in prefixes:
            if clean_version.startswith(prefix):
                clean_version = clean_version[len(prefix):].strip()
                break
        
        clean_version = clean_version.replace(' ', '').replace('-', '').replace('_', '')
        
        return clean_version
    
    def compare_versions(self, latest_version):
        try:
            current = version.parse(self.current_version)
            latest = version.parse(self.parse_version(latest_version))
            
            return latest > current, str(latest)
        except Exception as e:
            print(f"     {R}Error comparando versiones: {str(e)}{N}")
            return False, latest_version
    
    def get_download_assets(self, release_data):
        assets = release_data.get('assets', [])
        
        exe_asset = None
        zip_asset = None
        appimage_asset = None
        deb_asset = None
        
        for asset in assets:
            name = asset['name'].lower()
            if name.endswith('.exe') and self.sistema == "windows":
                exe_asset = asset
            elif name.endswith('.zip') and 'source' not in name:
                zip_asset = asset
            elif name.endswith('.appimage') and self.sistema == "linux":
                appimage_asset = asset
            elif name.endswith('.deb') and self.sistema == "linux":
                deb_asset = asset
     
        if not zip_asset:
            zip_asset = {
                'name': f"stelarys-v{self.parse_version(release_data['tag_name'])}-source.zip",
                'browser_download_url': release_data['zipball_url'],
                'size': 0
            }
        
        return exe_asset, zip_asset, appimage_asset, deb_asset
    
    def get_desktop_path(self):
        """Obtiene la ruta del escritorio según el sistema operativo"""
        if self.sistema == "windows":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:  # Linux/Ubuntu
            desktop_paths = [
                os.path.join(os.path.expanduser("~"), "Desktop"),
                os.path.join(os.path.expanduser("~"), "Escritorio"),
                os.path.join(os.path.expanduser("~"), "escritorio")
            ]
            
            for path in desktop_paths:
                if os.path.exists(path):
                    return path
            
           
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            os.makedirs(desktop_path, exist_ok=True)
            return desktop_path

    def download_file(self, url, filename, file_size=0):

        try:
            print(f"     {GRAY}({G}→{GRAY}) {W}Descargando {filename}...{N}")
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', file_size))
            downloaded = 0
            
            desktop_path = self.get_desktop_path()
            file_path = os.path.join(desktop_path, filename)
            
            print(f"     {GRAY}({G}→{GRAY}) {W}Guardando en: {desktop_path}{N}")
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r     {GRAY}[{G}{'█' * int(progress // 5):<20}{GRAY}] {progress:.1f}%{N}", end="")
            
            print(f"\n     {GRAY}({G}#{GRAY}) {W}Descarga completada: {file_path}{N}")
            return file_path
            
        except Exception as e:
            print(f"\n     {R}Error descargando archivo: {str(e)}{N}")
            return None
    
    def install_update(self, file_path, file_type="zip"):
        try:
            if file_type == "exe" and self.sistema == "windows":
                print(f"\n     {GRAY}({G}→{GRAY}) {W}Ejecutando instalador...{N}")
                print(f"     {YELLOW}El programa se cerrará para aplicar la actualización{N}")
                
                subprocess.Popen([file_path], shell=True)
                input(f"\n     {GRAY}Presiona Enter para cerrar el programa...{N}")
                sys.exit(0)
                
            elif file_type == "appimage" and self.sistema == "linux":
                print(f"\n {GRAY}({G}→{GRAY}) {W}Configurando AppImage...{N}")
                
                os.chmod(file_path, 0o755)
                
                print(f"     {G}AppImage configurado correctamente{N}")
                print(f"     {YELLOW}Ubicación: {file_path}{N}")
                print(f"     {GRAY}Puedes ejecutarlo directamente desde el escritorio{N}")
                
                
                run_now = input(f"\n {GRAY}({G}?{GRAY}) {W}¿Ejecutar la nueva versión ahora? (s/n): {N}").lower()
                if run_now in ['s', 'si', 'y', 'yes']:
                    subprocess.Popen([file_path])
                    sys.exit(0)
                
                return True
                
            elif file_type == "deb" and self.sistema == "linux":
                print(f"\n {GRAY}({G}→{GRAY}) {W}Instalando paquete .deb...{N}")
                print(f" {YELLOW}Se requieren permisos de sudo{N}")
                
                
                install_cmd = f"sudo dpkg -i '{file_path}'"
                print(f"     {GRAY}Ejecutando: {install_cmd}{N}")
                
                result = subprocess.run(install_cmd, shell=True)
                if result.returncode == 0:
                    print(f"     {G}Instalación completada correctamente{N}")
                   
                    subprocess.run("sudo apt-get install -f -y", shell=True)
                    return True
                else:
                    print(f"     {R}Error en la instalación del paquete .deb{N}")
                    return False
                
            else:
                
                print(f"\n     {GRAY}({G}→{GRAY}) {W}Extrayendo actualización...{N}")
                
                current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                backup_dir = os.path.join(current_dir, f"backup_{self.current_version}")
                
                # Crear backup
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                
                os.makedirs(backup_dir, exist_ok=True)
                
               
                important_files = ['config.json', 'settings.ini', 'data', '.env']
                for item in important_files:
                    src_path = os.path.join(current_dir, item)
                    if os.path.exists(src_path):
                        try:
                            if os.path.isdir(src_path):
                                shutil.copytree(src_path, os.path.join(backup_dir, item))
                            else:
                                shutil.copy2(src_path, backup_dir)
                            print(f"     {G}Backup: {item}{N}")
                        except Exception as e:
                            print(f"     {YELLOW}Advertencia backup {item}: {str(e)}{N}")
                
              
                extract_dir = os.path.join(os.path.dirname(file_path), "stelarys_update")
                if os.path.exists(extract_dir):
                    shutil.rmtree(extract_dir)
                
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
                
                extracted_items = os.listdir(extract_dir)
                if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_dir, extracted_items[0])):
                    source_dir = os.path.join(extract_dir, extracted_items[0])
                else:
                    source_dir = extract_dir
                
                
                for item in os.listdir(source_dir):
                    src = os.path.join(source_dir, item)
                    dst = os.path.join(current_dir, item)
                    
                    if os.path.isdir(src):
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                
                
                for item in important_files:
                    backup_path = os.path.join(backup_dir, item)
                    restore_path = os.path.join(current_dir, item)
                    
                    if os.path.exists(backup_path):
                        try:
                            if os.path.isdir(backup_path):
                                if os.path.exists(restore_path):
                                    shutil.rmtree(restore_path)
                                shutil.copytree(backup_path, restore_path)
                            else:
                                shutil.copy2(backup_path, restore_path)
                            print(f" {G}Restaurado: {item}{N}")
                        except Exception as e:
                            print(f" {YELLOW}Advertencia restaurando {item}: {str(e)}{N}")
                
               
                shutil.rmtree(extract_dir, ignore_errors=True)
                
                print(f"     {G}Actualización aplicada correctamente{N}")
                print(f"     {GRAY}Backup guardado en: {backup_dir}{N}")
                print(f"     {YELLOW}Reinicia el programa para completar la actualización{N}")
                
                return True
                
        except Exception as e:
            print(f"     {R}Error instalando actualización: {str(e)}{N}")
            return False
    
    def check_for_updates(self):
        print(f"\n     {GRAY}({G}*{GRAY}) {W}Sistema de Actualizaciones Automáticas{N}")
        print(f"      {R}- {W}Versión Actual: {C}v{self.current_version}{N}")
        print(f"      {R}- {W}Repositorio: {C}{self.repo_owner}/{self.repo_name}{N}")
        
        
        release_data = self.get_latest_release()
        if not release_data:
            print(f"     {R}No se pudo verificar actualizaciones{N}")
            return False
        
        latest_version = release_data['tag_name']
        release_name = release_data['name']
        release_notes = release_data['body'][:200] + "..." if len(release_data['body']) > 200 else release_data['body']
        
        print(f"      {R}- {W}Última Versión: {C}{latest_version}{N}")
        
       
        has_update, clean_latest = self.compare_versions(latest_version)
        
        if not has_update:
            print(f"\n     {GRAY}({G}✓{GRAY}) {W}Ya tienes la última versión instalada{N}")
            time.sleep(2)
            return True
        
        
        print(f"\n     {GRAY}({G}!{GRAY}) {W}¡Nueva actualización disponible!{N}")
        print(f"      {R}- {W}Versión: {C}{latest_version}{N}")
        print(f"      {R}- {W}Nombre: {C}{release_name}{N}")
        
        if release_notes.strip():
            print(f"      {R}- {W}Notas: {GRAY}{release_notes}{N}")
        
       
        exe_asset, zip_asset, appimage_asset, deb_asset = self.get_download_assets(release_data)
        
        print(f"\n     {GRAY}({G}?{GRAY}) {W}Opciones de descarga disponibles:{N}")
        
        options = []
        
      
        if self.sistema == "windows":
            if exe_asset:
                size_mb = exe_asset['size'] / (1024 * 1024) if exe_asset['size'] > 0 else 0
                print(f"       {G}1.{N} {W}Instalador (.exe) - {C}{size_mb:.1f} MB{N} {GRAY}(Recomendado){N}")
                options.append(('exe', exe_asset))
        
        
        elif self.sistema == "linux":
            if deb_asset:
                size_mb = deb_asset['size'] / (1024 * 1024) if deb_asset['size'] > 0 else 0
                option_num = len(options) + 1
                print(f"       {G}{option_num}.{N} {W}Paquete Debian (.deb) - {C}{size_mb:.1f} MB{N} {GRAY}(Recomendado para Ubuntu){N}")
                options.append(('deb', deb_asset))
            
            if appimage_asset:
                size_mb = appimage_asset['size'] / (1024 * 1024) if appimage_asset['size'] > 0 else 0
                option_num = len(options) + 1
                print(f" {G}{option_num}.{N} {W}AppImage (.appimage) - {C}{size_mb:.1f} MB{N} {GRAY}(Portable){N}")
                options.append(('appimage', appimage_asset))
        
       
        if zip_asset:
            size_mb = zip_asset['size'] / (1024 * 1024) if zip_asset['size'] > 0 else 0
            option_num = len(options) + 1
            print(f"       {G}{option_num}.{N} {W}Código fuente (.zip) - {C}{size_mb:.1f} MB{N} {GRAY}(Manual){N}")
            options.append(('zip', zip_asset))
        
        print(f"       {G}{len(options) + 1}.{N} {W}Cancelar actualización{N}")
        
      
        try:
            choice = input(f"\n      {GRAY}({G}?{GRAY}) {W}Selecciona una opción (1-{len(options) + 1}): {N}")
            choice_idx = int(choice) - 1
            
            if choice_idx == len(options):
                print(f"     {YELLOW}Actualización cancelada{N}")
                return False
            
            if 0 <= choice_idx < len(options):
                download_type, asset = options[choice_idx]
                
               
                desktop_path = self.get_desktop_path()
                print(f"\n     {GRAY}Se descargará en: {desktop_path}{N}")
                confirm = input(f" {GRAY}({G}?{GRAY}) {W}¿Confirmar descarga de {asset['name']}? (s/n): {N}").lower()
                if confirm not in ['s', 'si', 'y', 'yes']:
                    print(f" {YELLOW}Actualización cancelada{N}")
                    return False
                
               
                file_path = self.download_file(
                    asset['browser_download_url'], 
                    asset['name'], 
                    asset['size']
                )
                
                if file_path:
                   
                    return self.install_update(file_path, download_type)
                else:
                    print(f"     {R}Error en la descarga{N}")
                    return False
            else:
                print(f"     {R}Opción inválida{N}")
                return False
                
        except (ValueError, KeyboardInterrupt):
            print(f"\n     {YELLOW}Actualización cancelada{N}")
            return False


def update_system(current_version="2.0.0", repo_owner="Pabloescobarxde", repo_name="Stelarys-V2"):
    """
    Args:
        current_version (str): 
        repo_owner (str):
        repo_name (str):
    """
    try:
        updater = GitHubUpdater(repo_owner, repo_name, current_version)
        return updater.check_for_updates()
    except Exception as e:
        print(f"     {R}Error en el sistema de actualizaciones: {str(e)}{N}")
        return False
