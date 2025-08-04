from stelarys.src.utiles.imports import *

class Command:
    def __init__(self):
        self.name = 'scan'
        self.arguments: list = ['ip_address']
        self.should_exit = False

    def validate_arguments(self, arguments: list):
        if len(arguments) == 0:
            return False
        return True    

    def load_webhook_url(self):
        try:
            webhook_path = "stelarys/config/webhook.txt"
            if os.path.exists(webhook_path):
                with open(webhook_path, 'r') as file:
                    webhook_url = file.read().strip()
                    return webhook_url if webhook_url else None
            return None
        except:
            return None

    def send_webhook(self, webhook_url, data):
        try:
            requests.post(webhook_url, json=data, timeout=5)
        except:
            pass  # Silenciosamente ignora errores

    def check_minecraft_server(self, ip, port):
        try:
            ip_port = f"{ip}:{port}"
            response = requests.get(f"https://api.mcsrvstat.us/3/{ip_port}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('online', False):
                    motd = data.get('motd', {}).get('clean', ['N/A'])[0] if data.get('motd') else 'N/A'
                    version = data.get('version', 'N/A')
                    players = data.get('players', {}).get('online', 0)
                    max_players = data.get('players', {}).get('max', 0)
                    mods = len(data.get('mods', {}).get('names', [])) if data.get('mods') else 0
                    software = data.get('software', 'N/A')
                    
                    print(f'           {GRAY}({G}#{GRAY}) {GRAY}→ {W}Servidor Minecraft Detectado!')
                    print(f'           {GRAY}({G}#{GRAY}) {GRAY}→ {W}Ip:Puerto{GRAY} - {LR}{ip_port}')
                    print(f'           {GRAY}({G}#{GRAY}) {GRAY}→ {W}Motd{GRAY} - {motd}')
                    print(f'           {GRAY}({G}#{GRAY}) {GRAY}→ {W}Versión{GRAY} - {LR}{version}')
                    print(f'           {GRAY}({G}#{GRAY}) {GRAY}→ {W}Jugadores{GRAY} - {LR}{players} / {max_players}')
                    print(f'           {GRAY}({G}#{GRAY}) {GRAY}→ {W}Mods{GRAY} - {LR}{mods}')
                    print(f'           {GRAY}({G}#{GRAY}) {GRAY}→ {W}Software{GRAY} - {LR}{software}')
                    
                    
                    webhook_url = self.load_webhook_url()
                    if webhook_url:
                        webhook_data = {
                            "ip_port": ip_port,
                            "motd": motd,
                            "version": version,
                            "players": f"{players}/{max_players}",
                            "mods": mods,
                            "software": software
                        }
                        self.send_webhook(webhook_url, webhook_data)
                    
                    return True
            return False
        except:
            return False

    def scan_ip(self, ip_address: str, ip_number: int):
        if self.should_exit:
            return
            
        print(f'         {GRAY}({O}!{GRAY}) {W}Scaneando Ip {G}{ip_address}')
        print("")

        nmap_command = [
            'nmap',
            '-p', '100-150,151-165,166-199,200-250,251-265,266-299,300-350,351-365,366-399,400-450,451-465,466-499,500-550,551-565,566-599,600-650,651-665,666-699,700-750,751-765,766-799,800-850,851-865,866-899,900-950,951-965,966-999,1000-1100,1101-1165,1166-1999,2000-2200,2201-2265,2266-2999,3000-3300,3301-3365,3366-3999,4000-4400,4401-4465,4466-4999,5000-5500,5501-5565,5566-5999,6000-6600,6601-6665,6666-6999,7000-7700,7701-7765,7766-7999,8000-8800,8801-8865,8866-8999,9000-9900,9901-9965,9966-9999,10000-15500,15501-15565,15566-19999,20000-25500,25501-25565,25566-29999,30000-35500,35501-35565,35566-39999,40000-45500,45501-45565,45566-49999,50000-55500,55501-55565,55566-59999,60000-65500,65501-65535',
            '-T5',
            '-A',
            '-v',
            '-Pn',
            '--min-hostgroup', '8',
            '--max-hostgroup', '8',
            ip_address
        ]

        try:
            process = subprocess.Popen(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            port_protocol_pattern = re.compile(r'Discovered open port (\d+)/(\w+) on \d+\.\d+\.\d+\.\d+')
            
            try:
                for line in process.stdout:
                    if self.should_exit:
                        process.terminate()
                        break
                        
                    match = port_protocol_pattern.search(line)
                    if match:
                        port_number = match.group(1)
                        protocol = match.group(2)
                        port_protocol = f"{port_number}/{protocol}"
                        
                        print(f'           {GRAY}({G}#{GRAY}) {W}Puerto abierto: {G}{port_protocol} {GRAY}/ {LR}{ip_address}')
                        
                      
                        if protocol.lower() == 'tcp':
                            self.check_minecraft_server(ip_address, port_number)
            except:
                pass

            if not self.should_exit:
                process.wait()
            else:
                process.terminate()
                process.wait()
            
            if not self.should_exit:
                print('')
                print(f'         {GRAY}({LR}#{GRAY}) {W}Scaneo de la IP {LR}{ip_number} {W}ha finalizado')
                print('')

        except Exception as e:
            if not self.should_exit:
                print('')
                print(f'         {GRAY}({LR}#{GRAY}) {W}Error durante el escaneo de {LR}{ip_address}: {str(e)}')
                print('')

    def signal_handler(self, signum, frame):
        print('')
        print(f'         {GRAY}({R}!{GRAY}) {W}Interrumpiendo escaneo...')
        print("")
        self.should_exit = True
        sys.exit(0)

    def clean_input(self, input_str):
       
        if input_str.startswith('"') and input_str.endswith('"'):
            return input_str[1:-1]
        elif input_str.startswith("'") and input_str.endswith("'"):
            return input_str[1:-1]
        return input_str

    def is_file_path(self, input_str):
        return (os.path.exists(input_str) or 
                input_str.endswith(('.txt', '.list', '.ips')) or
                '/' in input_str or '\\' in input_str)

    def run(self, arguments: list):

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        if not self.validate_arguments(arguments):
            print("")
            print(f"      {GRAY}({R}#{GRAY}) {W}Inicia un scaneo de puertos con NMAP")
            print("")
            print(f"      {GRAY}({G}!{GRAY}) {O}Ejemplos de como usar el comando")
            print("")
            print(f"        {GRAY}→ {W}scan {G}quickland.net")
            print(f"        {GRAY}→ {W}scan {G}\"ips.txt\"")
            print(f"        {GRAY}→ {W}scan {G}'/path/to/ips.txt'")
            print("")
            print(f"      {GRAY}({G}#{GRAY}) {GRAY}→ {W} Una vez usada te dará los puertos abiertos y detectará servidores de Minecraft")
            print("")
            return

        print('')
        ip_address_input = self.clean_input(arguments[0])

        if not ip_address_input:
            print("")
            print(f"      {GRAY}({R}#{GRAY}) {W}Input vacío proporcionado")
            print("")
            return

        if self.is_file_path(ip_address_input):
            try:
                with open(ip_address_input, 'r') as file:
                    ip_addresses = [line.strip() for line in file.readlines() if line.strip()]
                
                if not ip_addresses:
                    print(f'         {GRAY}({R}#{GRAY}) {W}El archivo está vacío o no contiene IPs válidas')
                    return
                
                print(f'         {GRAY}({O}!{GRAY}) {W}Escaneando {G}{len(ip_addresses)} {W}IPs desde el archivo...')
                print('')
                
                for index, ip in enumerate(ip_addresses, start=1):
                    if self.should_exit:
                        break
                    if ip:  
                        self.scan_ip(ip, index)
                        
            except FileNotFoundError:
                print('')
                print(f'         {GRAY}({R}#{GRAY}) {W}Archivo no encontrado: {R}{ip_address_input}')
                print('')
            except Exception as e:
                print('')
                print(f'         {GRAY}({R}#{GRAY}) {W}Error al leer el archivo de IPs: {R}{str(e)}')
                print('')
        else:
           
            self.scan_ip(ip_address_input, 1)