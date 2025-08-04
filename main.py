import sys
import os
import platform

from stelarys.startrun import cargador


def set_console_title(title: str):
    system = platform.system()
    if system == "Windows":
        os.system(f"title {title}")
    else:
        print(f"\033]0;{title}\007", end='', flush=True)

def main():
    
    set_console_title("Stelarys / 2.0.0")
    cargador()
    

if __name__ == "__main__":
    main()
