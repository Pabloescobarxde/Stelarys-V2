from stelarys.src.utiles.imports import *



CURRENT_VERSION = "2.0.0"

def checker():
    checker_art = [
        "",
        "",
        "",
        "",
        " ▄▀▀▀▀▄  ▄▀▀▀█▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄      ▄▀▀█▄   ▄▀▀▄▀▀▀▄  ▄▀▀▄ ▀▀▄  ▄▀▀▀▀▄ ",
        "█ █   ▐ █    █  ▐ ▐  ▄▀   ▐ █    █      ▐ ▄▀ ▀▄ █   █   █ █   ▀▄ ▄▀ █ █   ▐ ",
        "   ▀▄   ▐   █       █▄▄▄▄▄  ▐    █        █▄▄▄█ ▐  █▀▀█▀  ▐     █      ▀▄   ",
        "▀▄   █     █        █    ▌      █        ▄▀   █  ▄▀    █        █   ▀▄   █  ",
        " █▀▀▀    ▄▀        ▄▀▄▄▄▄     ▄▀▄▄▄▄▄▄▀ █   ▄▀  █     █       ▄▀     █▀▀▀   ",
        " ▐      █          █    ▐     █         ▐   ▐   ▐     ▐       █      ▐      ",
        "        ▐          ▐          ▐                               ▐             "
    ]

    terminal_size = shutil.get_terminal_size()
    terminal_width = terminal_size.columns
    """ 
    terminal_height = terminal_size.lines
    art_height = len(checker_art)
    top_padding = max((terminal_height - art_height) // 2, 0)
    print("\n" * top_padding, end="")
   """
    for line in checker_art:
        padding = max((terminal_width - wcswidth(line)) // 2, 0)
        print(" " * padding + f"{R}{line}{N}")

    print("\n\n\n\n")
    print(f"     {GRAY}[{R}#{GRAY}]{W} Verificando actualizaciones pendientes... \n")
    check_dependencies()
    time.sleep(2)
    update_system()
    time.sleep(2)
    clear_console()
    Letra()
    menu()

if __name__ == "__main__":
    checker()
