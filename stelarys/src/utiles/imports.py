import time
import os   
import shutil
import sys
import datetime
import sys
import shutil
import json
import string
import importlib
import subprocess
import random
import ipaddress
import requests
import tempfile
import zipfile
import platform
import dns.resolver
import re
import threading
import socket
import urllib3
import signal


from urllib.parse import urlparse
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from pypresence import Presence
from packaging import version
from bs4 import BeautifulSoup
from wcwidth import wcswidth

from colorama import init, Fore, Style
from stelarys.src.utiles.clear import clear_console
from stelarys.src.utiles.colores import *
from stelarys.src.utiles.instalaciones import obtener_versiones
from stelarys.src.componentes.system_name import obtener_nombre_pc
from stelarys.src.comandos.connect import Command as ConnectCommand
from stelarys.src.comandos.shodan import Command as ShodanCommand
from stelarys.src.comandos.servidor import Command as ServerCommand
from stelarys.src.comandos.lookserver import Command as LookserverCommand
from stelarys.src.comandos.lookdns import Command as LookdnsCommand
from stelarys.src.comandos.jugador import jugadorCommand
from stelarys.src.comandos.denegar import denegarCommand
from stelarys.src.comandos.rutas import Command as RutasCommand
from stelarys.src.comandos.scan import Command as ScanCommand
from stelarys.src.comandos.webhook import Command as WebhookCommand
from stelarys.src.comandos.ayuda import help
from stelarys.src.componentes.sytem_info import get_system_info
from stelarys.src.utiles.get_appdata import get_appdata_path
from stelarys.src.update.dependencia import check_dependencies
from stelarys.src.interfaz.inicio import menu, Letra
from stelarys.src.utiles.clear import clear_console
from stelarys.src.update.actualizaciones import update_system

init()