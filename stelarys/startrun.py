import time
import os

from stelarys.src.banners.cargador import mostrar_banner
from stelarys.src.presence.rich_rpc import iniciar_rpc
from stelarys.src.banners.checker import checker
from stelarys.src.utiles.clear import clear_console
from stelarys.src.interfaz.inicio import Letra, menu

def cargador(): 

   os.system('cls' if os.name == 'nt' else 'clear')
   iniciar_rpc()      
   os.system('cls' if os.name == 'nt' else 'clear')
   mostrar_banner()  
   time.sleep(4)
   os.system('cls' if os.name == 'nt' else 'clear')
   checker()
