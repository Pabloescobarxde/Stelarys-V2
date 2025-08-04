from stelarys.src.utiles.imports import *

def iniciar_rpc():

    CLIENT_ID = "1373326189586026547"
    START_TIME = int(time.time())

    rpc = Presence(CLIENT_ID)
    rpc.connect()

    rpc.update(
        details="🔥 Mejor Herramienta de minecraft",
        state="👿 Usando Stelarys",
        start=START_TIME,
        large_image="logotipo",
        large_text="Stelarys - Potencia total",
        small_image="r",
        small_text="El Mejor",
        buttons=[
            {"label": "Unirme al Discord", "url": "https://discord.gg/viperfinder"}
        ]
    )
