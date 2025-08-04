from stelarys.src.utiles.imports import *

def Letra():
    python_version, node_version = obtener_versiones()

    letra_arci = f"""
    
     {R}███████╗████████╗███████╗██╗      █████╗ ██████╗ ██╗   ██╗███████╗          {W}Version        {W}Viper
     {R}██╔════╝╚══██╔══╝██╔════╝██║     ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝           {M}↪ {G}2.0.0        {M}↪ {R}OFF
     {R}███████╗   ██║   █████╗  ██║     ███████║██████╔╝ ╚████╔╝ ███████╗                                    
     {W}╚════██║   ██║   ██╔══╝  ██║     ██╔══██║██╔══██╗  ╚██╔╝  ╚════██║          {W}Python        {W}NodesJS                
     {W}███████║   ██║   ███████╗███████╗██║  ██║██║  ██║   ██║   ███████║           {M}↪ {G}{python_version}      {M}↪ {R}{node_version}   
     {W}╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝                                      

      {GRAY}{W}Hola {LR}@{nombre_pc} {W}Bienvenido {GRAY}-{W} Comienza con {G} Help{GRAY}
    """
    print(letra_arci)
    

current_menu = 0


nombre_pc = obtener_nombre_pc()

def menu():
    global current_menu
    while True:
        try:
            opcion = input(Fore.RED +
                    f"      {R}Stelarys{LR}@{nombre_pc}" +
                    f"{Style.RESET_ALL}:~$ "
                ).strip()

            if opcion == 'help':
                help()  

            if opcion in ['clear', 'cls', 'quieropene']: 
                clear_console()  
                Letra()
                menu()

            if opcion in ['exit', 'close']: 
                break

            elif opcion.startswith('shodan'):
                partes = opcion.strip().split()
                comando_shodan = ShodanCommand()
                if len(partes) == 1:
                    comando_shodan.run([])
                else:
                    argumentos = partes[1:]
                    comando_shodan.run(argumentos)

                time.sleep(1)

            elif opcion.startswith('server'):
                partes = opcion.strip().split()
                comando_server = ServerCommand()
                if len(partes) == 1:
                    comando_server.run([])
                else:
                    argumentos = partes[1:]
                    comando_server.run(argumentos)

            elif opcion.startswith('lookserver'):
                argumentos = opcion.split(' ')[1:]
                comando_lookserver = LookserverCommand()
                comando_lookserver.run(argumentos)
                time.sleep(3)

                time.sleep(1)

            elif opcion.startswith('lookdns'):
                argumentos = opcion.split(' ')[1:]
                comando_lookdns = LookdnsCommand()
                comando_lookdns.run(argumentos)
                time.sleep(3)

            if opcion.startswith('jugador'):
              argumentos = opcion.split(' ')[1:]
              comando_jugador = jugadorCommand()
              comando_jugador.run(argumentos)

            if opcion.startswith('denegar'):
              argumentos = opcion.split(' ')[1:]
              comando_denegar = denegarCommand()
              comando_denegar.run(argumentos)

            elif opcion.startswith('scan'):
                argumentos = opcion.split(' ')[1:]
                comando_scan = ScanCommand()
                comando_scan.run(argumentos)
                time.sleep(3)

            elif opcion.startswith('rutas'):
                argumentos = opcion.split(' ')[1:]
                comando_rutas = RutasCommand()
                comando_rutas.run(argumentos)
                time.sleep(3)

            elif opcion.startswith('url'):
                argumentos = opcion.split(' ')[1:]
                comando_webhook = WebhookCommand()
                comando_webhook.run(argumentos)
                time.sleep(3)

            elif opcion.startswith('connect'):
                argumentos = opcion.split(' ')[1:]
                comando_conectart = ConnectCommand()
                comando_conectart.run(argumentos)
                time.sleep(3)


            else:
                input(f"""
      {R}~>:${nombre_pc}{LR}@{LR}Opcion Invalida
""")
        except KeyboardInterrupt:
            print("")
            print(f"\n\n      {R}~>:$ Reiniciando stelarys...")
            print("")
            break  
        
        except Exception as e:
            print(f"      {R}~>:$ Consultar en Pablo ({e})")
            input("...")
            clear_console()
            Letra()
            menu()