from stelarys.src.utiles.imports import *


minecraft_color_codes = {
    '0': '\033[30m', '1': '\033[34m', '2': '\033[32m', '3': '\033[36m',
    '4': '\033[31m', '5': '\033[35m', '6': '\033[33m', '7': '\033[37m',
    '8': '\033[90m', '9': '\033[94m', 'a': '\033[92m', 'b': '\033[96m',
    'c': '\033[91m', 'd': '\033[95m', 'e': '\033[93m', 'f': '\033[97m',
    'r': '\033[0m',  'l': '\033[1m',  'n': '\033[4m',
    'o': '\033[3m',  'm': '\033[9m'
}


def apply_minecraft_colors(text):
    pattern = re.compile(r'§([0-9a-frlomn])', re.IGNORECASE)
    result = ""
    index = 0

    for match in pattern.finditer(text):
        start, end = match.span()
        code = match.group(1).lower()
        result += text[index:start]
        result += minecraft_color_codes.get(code, '')
        index = end

    result += text[index:]
    result += '\033[0m'
    return result


class Command:
    def __init__(self):
        self.name = 'server'
        self.arguments = ['ip']

    def get_server_info(self, ip):
        try:
            response = requests.get(f"https://api.mcsrvstat.us/3/{ip}", timeout=10)
            server_data = response.json()
        except Exception as e:
            print(f"\n        {GRAY}({RED}✘{GRAY}) Error al consultar la API: {e}\n")
            return

        if response.status_code != 200 or not server_data.get('online'):
            print(f"\n        {GRAY}({R}✘{GRAY}) El servidor está fuera de linea o no se pudo obtener la informacion.\n")
            return

        ip_port = f"{server_data.get('ip')}:{server_data.get('port')}"
        motd_raw = "\n".join(server_data.get('motd', {}).get('raw', []))
        motd = apply_minecraft_colors(motd_raw)

        version_field = server_data.get('version', {})
        if isinstance(version_field, dict):
            version_name = version_field.get('name', 'Desconocido')
            protocol = version_field.get('version', 'Desconocido')
            version = f"{protocol} / {version_name}"
        else:
            version = str(version_field)

        players = server_data.get('players', {}).get('online', 0)
        max_players = server_data.get('players', {}).get('max', 0)
        mods = server_data.get('mods', {}).get('names', [])
        software = server_data.get('software', 'Desconocido')

        print(f"""         {GRAY}({R}*{GRAY}) {W}Informacion Encontrada {W}

         {GRAY}({G}#{GRAY}) {GRAY}→ {W}Ip:Puerto{GRAY} - {LR}{ip_port}
         {GRAY}({G}#{GRAY}) {GRAY}→ {W}Motd{GRAY} - {motd}
         {GRAY}({G}#{GRAY}) {GRAY}→ {W}Versión{GRAY} - {LR}{version}
         {GRAY}({G}#{GRAY}) {GRAY}→ {W}Jugadores{GRAY} - {LR}{players} / {max_players}
         {GRAY}({G}#{GRAY}) {GRAY}→ {W}Mods{GRAY} - {LR}{mods}
         {GRAY}({G}#{GRAY}) {GRAY}→ {W}Software{GRAY} - {LR}{software}
        """)

    def validate_arguments(self, arguments):
        return len(arguments) == 1

    def run(self, arguments):
        if not self.validate_arguments(arguments):
            print("")
            print(f"      {GRAY}({R}#{GRAY}) {W}Obten la status de un servidor de minecraft con la api {R}mcsrvstat")
            print("")
            print(f"      {GRAY}({G}!{GRAY}) {O}Ejemplos de como usar el comando")
            print("")
            print(f"        {GRAY}→ {W}server {G}mc.universocraft.com")
            print("")
            print(f"      {GRAY}({G}#{GRAY}) {GRAY}→ {W} Una ves usada te dara la status del servidor.")
            print("")
            return
        ip = arguments[0]
        print(f"\n        {GRAY}({O}!{GRAY}) {W}Obteniendo informacion para {G}{ip}\n")
        self.get_server_info(ip)
        time.sleep(1)
