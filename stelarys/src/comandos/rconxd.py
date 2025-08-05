from mccolors import mcwrite, mcreplace
from typing import Union
from mcrcon import MCRcon, MCRconException

class Command:
    def __init__(self):
        self.name: str = 'rcon'
        self.arguments: list = ['ip', 'puerto', 'contraseña']
        self.passwords: list = []

    def run(self, argumentos: list) -> None:
        """
        Método para ejecutar el comando

        Args:
            argumentos (list): Los argumentos para ejecutar el comando
        """

        if len(argumentos) < 2:
            mcwrite("")
            mcwrite(" &f&l- &8&l[&f&lArgumentos inválidos!&8&l] &f- &8&l[&frcon <ip:puerto> <contraseña>&8&l]")
            return

        ip_address: str = argumentos[0].split(':')[0]
        port: str = argumentos[0].split(':')[1]
        rcon_password: str = argumentos[1]
        mcr: Union[MCRcon, None] = None

        try:
            with MCRcon(host=ip_address, password=rcon_password, port=int(port), timeout=30) as mcr:
                mcwrite("")
                mcwrite(" - &8&l[&f&lConectado exitosamente&8&l]")

                while True:
                    mcwrite("")
                    comando: str = input(mcreplace(" - &8&l[&f&lEscribe un comando (o .exit)&8&l]: "))

                    if comando == '.exit':
                        mcwrite(" - &8&l[&f&lDesconectado del servidor&8&l]")
                        mcr.disconnect()
                        break

                    respuesta: str = mcr.command(comando)
                    mcwrite(f" - &8&l[&f&lRespuesta: &c{respuesta}&8&l]")

        except TimeoutError:
            mcwrite("")
            mcwrite(" - &8&l[&f&lTiempo de espera agotado al intentar conectar&8&l]")

        except ConnectionRefusedError:
            mcwrite("")
            mcwrite(" - &8&l[&f&lConexión rechazada por el servidor&8&l]")

        except MCRconException:
            mcwrite("")
            mcwrite(" - &8&l[&f&lContraseña RCON incorrecta&8&l]")

        except KeyboardInterrupt:
            if mcr:
                mcr.disconnect()
                mcwrite("")
            mcwrite(" - &8&l[&f&lDesconectado del servidor por el usuario&8&l]")

        except Exception:
            # Muestra un mensaje genérico sin registrar detalles
            mcwrite("")
            mcwrite(" - &8&l[&f&lOcurrió un error inesperado, por favor revisa la configuracion&8&l]")
