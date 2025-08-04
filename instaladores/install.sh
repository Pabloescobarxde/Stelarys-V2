#!/bin/bash

echo -e "\e[36mIniciando el proceso de instalación...\e[0m"

# Función para verificar respuesta afirmativa
function es_si() {
    [[ "$1" =~ ^[YySs]$ ]]
}

# Preguntar por Python
read -p "¿Quieres instalar Python? (y/s para sí, cualquier otra tecla para no): " instalar_python
if es_si "$instalar_python"; then
    echo -e "\e[33mInstalando Python...\e[0m"
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Preguntar por Node.js
read -p "¿Quieres instalar Node.js? (y/s para sí, cualquier otra tecla para no): " instalar_node
if es_si "$instalar_node"; then
    echo -e "\e[33mInstalando Node.js...\e[0m"
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
fi

# Verificación
echo -e "\n\e[36mVerificando instalaciones...\e[0m"

if es_si "$instalar_python"; then
    echo -n "Python: "; python3 --version
    echo -n "Pip: "; pip3 --version
fi

if es_si "$instalar_node"; then
    echo -n "Node.js: "; node -v
    echo -n "NPM: "; npm -v
fi

echo -e "\n✅ \e[32mInstalación completada.\e[0m"
