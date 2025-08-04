from stelarys.src.utiles.imports import *

minecraft_color_codes = {
    '0': '\033[30m', '1': '\033[34m', '2': '\033[32m', '3': '\033[36m',
    '4': '\033[31m', '5': '\033[35m', '6': '\033[33m', '7': '\033[37m',
    '8': '\033[90m', '9': '\033[94m', 'a': '\033[92m', 'b': '\033[96m',
    'c': '\033[91m', 'd': '\033[95m', 'e': '\033[93m', 'f': '\033[97m',
    'r': '\033[0m',  'l': '\033[1m',  'n': '\033[4m',
    'o': '\033[3m',  'm': '\033[9m'
}

class Command:
    def __init__(self):
        self.name = 'Lookserver'
        self.arguments = ['Lookserver, modalidad, cuanto servidores']
        self.found_domains = set()
        self.results = []

    def apply_minecraft_colors(self, text):
        text = re.sub(r'§#[0-9A-Fa-f]{6}', '', text)
        for code, ansi in minecraft_color_codes.items():
            text = text.replace(f"§{code}", ansi)
        return text + minecraft_color_codes['r']

    def get_server_info(self, ip, server_number, online_count, offline_count):
        response = requests.get(f"https://api.mcsrvstat.us/3/{ip}")
        if response.status_code != 200:
            offline_count += 1
            print(f"      {GRAY}({R}✘{GRAY}) El servidor {ip} está fuera de línea.")
            return online_count, offline_count, None

        server_data = response.json()
        if not server_data.get('online'):
            offline_count += 1
            print(f"      {GRAY}({R}✘{GRAY}) El servidor {ip} está fuera de línea.")
            return online_count, offline_count, None

        ip_port = f"{server_data.get('ip')}:{server_data.get('port')}"
        motd_list = server_data.get('motd', {}).get('raw', [])
        motd_raw = "\n".join(motd_list)
        motd = self.apply_minecraft_colors(motd_raw)

        version = server_data.get('version')

       
        protocol_info = server_data.get('protocol')
        if isinstance(protocol_info, dict):
            protocol_version = protocol_info.get('name', 'Desconocido')
        elif isinstance(protocol_info, list) and len(protocol_info) > 0:
            protocol_version = str(protocol_info[0])
        elif isinstance(protocol_info, str):
            protocol_version = protocol_info
        else:
            protocol_version = 'Desconocido'

        players = server_data.get('players', {}).get('online', 0)
        max_players = server_data.get('players', {}).get('max', 0)
        mods = server_data.get('mods', {}).get('names', [])
        software = server_data.get('software', 'Desconocido')

        print(f"""
          {GRAY}({G}#{GRAY}) {W}Ip:Puerto {GRAY}- {LR}{ip_port}{GRAY}
          {GRAY}({G}#{GRAY}) {W}Motd {GRAY}- {LR}{motd}{GRAY}
          {GRAY}({G}#{GRAY}) {W}Version {GRAY}- {LR}{version}{GRAY}
          {GRAY}({G}#{GRAY}) {W}Protocolo {GRAY}- {LR}{protocol_version}{GRAY}
          {GRAY}({G}#{GRAY}) {W}Jugadores {GRAY}- {LR}{players}/{max_players}{GRAY}
          {GRAY}({G}#{GRAY}) {W}Mods {GRAY}- {LR}{mods}{GRAY}
          {GRAY}({G}#{GRAY}) {W}Server Hecho {GRAY}- {LR}{software}{GRAY}
          {GRAY}({G}#{GRAY}) {W}Server Numero {GRAY}- {LR}{server_number}{GRAY}
        """)

        server_info = {
            "ip_port": ip_port,
            "motd": motd,
            "version": version,
            "protocol": protocol_version,
            "players": {
                "online": players,
                "max": max_players
            },
            "mods": mods,
            "software": software,
            "server_number": server_number
        }

        online_count += 1
        return online_count, offline_count, server_info

    def obtener_ips(self, modalidad, pagina):
        url = f"https://minecraftservers.org/search/{modalidad}/{pagina}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"          {R}Error al conectar con la página. Consulta a Pablo.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        server_listings = soup.find_all('div', class_='server-listing')

        ips = []
        for server in server_listings:
            ip_tag = server.find('div', class_='url')
            if ip_tag:
                ip = ip_tag.text.strip()
                ips.append(ip)

        return ips

    def obtener_ips_totales(self, modalidad, cantidad):
        ips_totales = []
        intentos = 0
        max_intentos = 50

        while len(ips_totales) < cantidad and intentos < max_intentos:
            pagina = random.randint(1, 50)
            ips = self.obtener_ips(modalidad, pagina)
            if ips:
                ips_totales.extend(ips)
            intentos += 1

        return ips_totales[:cantidad]

    def obtener_servidores(self, modalidad, cantidad, guardar):
        print(f"\n         {GRAY}({GREEN}*{GRAY}){W} Buscando servidores {modalidad}...\n")
        ips = self.obtener_ips_totales(modalidad, cantidad)

        online_count = 0
        offline_count = 0
        servidores = []

        for idx, ip in enumerate(ips, 1):
            online_count, offline_count, server_info = self.get_server_info(ip, idx, online_count, offline_count)
            if server_info:
                servidores.append(server_info)

        print(f"\n        {GRAY}({GREEN}✓{GRAY}){W} Servidores online: {online_count} {GRAY}/ {W}Servidores offline: {offline_count}\n")

        if guardar:
            self.guardar_servidores(modalidad, servidores)

    def guardar_servidores(self, modalidad, servidores):
        if not os.path.exists("servidores"):
            os.makedirs("servidores")

        random_number = random.randint(1000, 9999)
        file_name = f"servidores/{modalidad}_{random_number}.json"

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(servidores, file, ensure_ascii=False, indent=4)

    def run(self, argumentos):
        if len(argumentos) > 1:
            modalidad = argumentos[0]
            try:
                cantidad = int(argumentos[1])
            except ValueError:
                print(f"      {GRAY}({R}#{GRAY}) {LR}Cantidad debe ser un número.")
                return

            guardar = input(f"\n        {GRAY}({LR}#{GRAY}){W} ¿Deseas guardar la búsqueda de datos? (s/n): ").strip().lower() == 's'
            self.obtener_servidores(modalidad, cantidad, guardar)
        else:
            print("")
            print(f"      {GRAY}({R}#{GRAY}) {W}Obten una lista de servidores")
            print("")
            print(f"      {GRAY}({G}!{GRAY}) {O}Ejemplos de como usar el comando")
            print("")
            print(f"        {GRAY}→ {W}lookserver {LR}Survival 10")
            print("")
            print(f"      {GRAY}({G}#{GRAY}) {GRAY}→ {W} Una ves usada te dara la lista de servidores")
            print("")
            return
