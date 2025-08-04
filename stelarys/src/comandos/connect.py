from stelarys.src.utiles.imports import *


class Command:
    def __init__(self):
        self.name = 'connect'
        self.arguments: list = ['nick', 'ip', 'port']

       
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', '..')
        )
        self.script_path = os.path.join(
            self.project_root, 'stelarys', 'JS', 'connect.js'
        )

    def validate_arguments(self, arguments: list):
        if len(arguments) != len(self.arguments):
            return False

        
        if not re.match(r'^([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|(\d{1,3}\.){3}\d{1,3})$', arguments[1]):
            return False

       
        if not arguments[2].isdigit() or not (0 <= int(arguments[2]) <= 65535):
            return False

        
        if not arguments[0].isalnum() or len(arguments[0]) > 16:
            return False

        return True

    def run(self, arguments: list):
        if not self.validate_arguments(arguments):
            print("")
            print(f"       {GRAY}({R}#{GRAY}) {W}Conecta un bot a un servidor de minecraft.")
            print("")
            print(f"       {GRAY}({G}!{GRAY}) {O}Pasos para usarlo:")
            print("")
            print(f"          {GRAY}→ {W}servidor {LY}Quickland.net{RESET}")
            print("")
            print(f"          {GRAY}→ {W}Connect Pablinikapuchini 179.41.13.72 25565{LY}{RESET}")
            print("")
            print("")
            print(f"       {GRAY}({G}→{GRAY}) {W}Una vez colocado el comando se conectara el bot (Recuerda que algunos svs tiene antibots)")
            print("")
            time.sleep(3)
            return



       
        try:
            subprocess.run(
                ['node', self.script_path, arguments[0], arguments[1], arguments[2]],
                check=True
            )
        except subprocess.CalledProcessError as e:
            pass