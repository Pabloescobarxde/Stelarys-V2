from stelarys.src.utiles.imports import *

WEBHOOK_REGEX = re.compile(
    r'^https:\/\/(discord|discordapp)\.com\/api\/webhooks\/\d+\/[\w-]+$'
)

class Command:
    def run(self, argumentos):
        ruta_config = 'stelarys/config/webhook.txt'
        directorio = os.path.dirname(ruta_config)

        if not argumentos:
            print("")
            print(f"       {GRAY}({R}#{GRAY}) {W}Coloca una webhook de discord (RQ para algunos comandos)")
            print("")
            print(f"       {GRAY}({G}!{GRAY}) {O}Ejemplos como puedes usarlo:")
            print("")
            print(f"          {GRAY}→ {W}Tutorial {LY}Youtube: Como crear una webhook{RESET}")
            print("")
            print("")
            print(f"       {GRAY}({G}→{GRAY}) {W}Una vez colocado el comando se enviara mensaje a la webhook de exito")
            print("")
            return
            return

        if not os.path.exists(directorio):
            os.makedirs(directorio)

        urls_validas = []
        for url in argumentos:
            url = url.strip()
            if WEBHOOK_REGEX.match(url):
                urls_validas.append(url)
            else:
                print(f"        {GRAY}({LR}#{GRAY}){W} URL invalida: {url}")

        if urls_validas:
            with open(ruta_config, 'w', encoding='utf-8') as f:
                for url in urls_validas:
                    f.write(url + '\n')

            embed_data = {
                "embeds": [
                    {
                        "author": {
                            "name": "Stelarys"
                        },
                        "title": "Webhook configurada con exito ✅",
                        "description": "La webhook ha sido registrada y configurada correctamente.",
                        "color": 0x00FF00  
                    }
                ]
            }

            for webhook_url in urls_validas:
                try:
                    requests.post(webhook_url, json=embed_data, timeout=5)
                except Exception:
                    pass

            print(f"        {GRAY}({GREEN}✓{GRAY}) {W}webhook colocada exitosamente.")
        else:
            print(f"        {GRAY}({LR}!{GRAY}){W} No se coloco ninguna webhook valida.")
