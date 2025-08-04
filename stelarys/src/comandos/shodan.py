from stelarys.src.utiles.imports import *

class Command:
    def __init__(self):
        self.name = 'shodan'
        self.arguments: list = ['ip o dominio']

    def get_ip(self, target):
        try:
            socket.inet_aton(target)
            return target
        except socket.error:
            try:
              
                return socket.gethostbyname(target)
            except socket.gaierror:
                return None

    def validate_arguments(self, arguments: list):
        return len(arguments) > 0

    def run(self, arguments: list):
        if not self.validate_arguments(arguments):
            print("")
            print(f"      {GRAY}({R}#{GRAY}) {W}Obten informacion sobre una ip con la api {R}shodan {O}Ipinfo")
            print("")
            print(f"      {GRAY}({G}!{GRAY}) {O}Ejemplos de como usar el comando")
            print("")
            print(f"        {GRAY}→ {W}shodan {LR}1.1.1.1")
            print("")
            print(f"      {GRAY}({G}#{GRAY}) {GRAY}→ {W} Una ves usada te dara la informacion sobre la ip.")
            print("")
            return

        target = arguments[0]
        print("")
        print(f"       {GRAY}({O}!{GRAY}) {W}Buscando información para {LR}{target}")

        ip_address = self.get_ip(target)

        if ip_address is None:
            print("")
            print(f"       {GRAY}({R}X{GRAY}) [{R}No se pudo resolver la dirección IP del objetivo.")
            return

        internetdb_url = f"https://internetdb.shodan.io/{ip_address}"
        response = requests.get(internetdb_url)

        print("")
        if response.status_code == 200:
            data = response.json()

            print(f"        {GRAY}({R}*{GRAY}) {W}Informacion Encontrada:")
            print("")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}IP {GRAY}- {LR}{data['ip']}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Hostnames {GRAY}- {LR}{', '.join(data['hostnames']) if data['hostnames'] else 'N/A'}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Puertos {GRAY}- {LR}{', '.join(map(str, data['ports'])) if data['ports'] else 'N/A'}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Vulnerabilidades {GRAY}- {LR}{', '.join(data['vulns']) if data['vulns'] else 'N/A'}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}CPEs {GRAY}- {LR}{', '.join(data['cpes']) if data['cpes'] else 'N/A'}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Etiquetas {GRAY}- {LR}{', '.join(data['tags']) if data['tags'] else 'N/A'}")

        else:
            print("")
            print(f"        {GRAY}({LY}!{GRAY}) {W}Error al consultar InternetDB, por favor verifica la direccion.")

        ipinfo_url = f"https://ipinfo.io/{ip_address}/json"
        ipinfo_response = requests.get(ipinfo_url)

        print("")
        if ipinfo_response.status_code == 200:
            ipinfo_data = ipinfo_response.json()
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}IP {GRAY}- {LR}{ipinfo_data.get('ip', 'N/A')}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Ciudad {GRAY}- {LR}{ipinfo_data.get('city', 'N/A')}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Región {GRAY}- {LR}{ipinfo_data.get('region', 'N/A')}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}País {GRAY}- {LR}{ipinfo_data.get('country', 'N/A')}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Código postal {GRAY}- {LR}{ipinfo_data.get('postal', 'N/A')}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Ubicación {GRAY}- {LR}{ipinfo_data.get('loc', 'N/A')}")
            print(f"        {GRAY}({G}#{GRAY}) {GRAY}→ {W}Organización {GRAY}- {LR}{ipinfo_data.get('org', 'N/A')}")
        else:
            print("")
            print(f"        {GRAY}({LY}!{GRAY}) {W}Error al obtener información de IPInfo.")

        print("")
