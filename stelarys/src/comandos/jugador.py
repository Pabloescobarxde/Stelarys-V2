from stelarys.src.utiles.imports import *

class jugadorCommand:

    def run(self, args):
        if not args:
            print("")
            print(f"       {GRAY}({R}#{GRAY}) {W}Obten informacion detallada de un jugador de Minecraft")
            print("")
            print(f"       {GRAY}({G}!{GRAY}) {O}Ejemplos como puedes usarlo:")
            print("")
            print(f"          {GRAY}→ {W}Jugador {LY}vmario{RESET}")
            print("")
            print("")
            print(f"       {GRAY}({G}→{GRAY}) {W}Una vez colocado el comando se buscara automaticamente la informacion")
            print("")
            return

        ruta_o_nick = args[0].strip("\"'") 

        if os.path.isfile(ruta_o_nick):
            with open(ruta_o_nick, "r", encoding="utf-8") as file:
                nicks = [line.strip().strip("\"'") for line in file if line.strip()]
            for nickname in nicks:
                self.procesar_jugador(nickname)
        else:
            self.procesar_jugador(ruta_o_nick)

    def procesar_jugador(self, nickname):
        print("")
        print(f"       {GRAY}({R}*{GRAY}) {W}Buscando resultados para {nickname}...")
        uuid, status = self.check_premium(nickname)
        history = self.get_username_history(uuid)
        self.display_results(nickname, uuid, status, history)

    def check_premium(self, nickname):
        api_url = f"https://api.mojang.com/users/profiles/minecraft/{nickname}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            uuid = data.get('id')
            return uuid, "premium"
        except requests.exceptions.RequestException:
            return None, "no premium"

    def get_username_history(self, uuid):
        if not uuid:
            return None

        url = f'https://laby.net/api/v3/user/{uuid}/profile'
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            data = response.json()
            if 'name_history' in data:
                return [entry['name'] for entry in data['name_history']]
            return None
        except requests.exceptions.RequestException:
            return None

    def display_results(self, nickname, uuid, status, history):
        name_history = f"{GRAY} →{W} ".join(history) if history else RED + "Sin historial"
        uuid_display = uuid if uuid else "?"

        uuid_color = RED if status == "no premium" else GREEN
        status_color = LR if status == "no premium" else LY

        print(f"""
        {GRAY}({GREEN}#{GRAY}) → {W}Nickname {GRAY}- {W}{nickname}
        {GRAY}({GREEN}#{GRAY}) → {W}Status {GRAY} - {status_color}{status.capitalize()}
        {GRAY}({GREEN}#{GRAY}) → {W}UUID {GRAY} - ({uuid_color}{uuid_display}{GRAY})
        {GRAY}({GREEN}#{GRAY}) → {W}Historial {GRAY} - ({W}{name_history}{GRAY})
""")
