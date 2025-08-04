# 🌟 Stelarys Tool

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Nmap](https://img.shields.io/badge/Nmap-4682B4?style=for-the-badge&logo=nmap&logoColor=white)
![Minecraft](https://img.shields.io/badge/Minecraft-62B47A?style=for-the-badge&logo=minecraft&logoColor=white)

![License](https://img.shields.io/badge/License-Custom-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge)

**🛡️ Herramienta avanzada de pentesting para Minecraft con tecnologías híbridas**

</div>

---

## 🌐 Contenido

- [📦 Instalación Rápida](#-instalación-rápida)
- [🔧 Instalación Manual](#-instalación-manual)
- [🔍 ¿Qué es Stelarys Tool?](#-qué-es-stelarys-tool)
- [🚀 Uso](#-uso)
- [📜 Licencia](#-licencia)
- [⚠️ Nota importante](#️-nota-importante)
- [🙏 Créditos](#-créditos)

---

## 📦 Instalación Rápida

### 🎯 Instalación Automática

**Stelarys Tool** se puede instalar automáticamente con todas sus dependencias:

#### 🐍 Usando pip (Python)
```bash
pip install stelarys
```

#### 📦 Usando npm (Node.js)
```bash
npm install stelarys
```

> [!TIP]
> Las instalaciones automáticas incluyen todas las dependencias necesarias y configuran el entorno automáticamente.

---

## 🔧 Instalación Manual

### 🛠️ Requisitos del Sistema

Antes de comenzar, asegúrate de tener instalado:

| Tecnología | Versión Recomendada | Obligatorio |
|------------|-------------------|-------------|
| **Python** | 3.11+ | ✅ |
| **Node.js** | 18+ | ✅ |
| **npm** | 9+ | ✅ |
| **Nmap** | 7.90+ | ✅ |

### 🐍 Instalación de Python

> [!IMPORTANT]
> **MUY IMPORTANTE**: Cuando instales Python, deberás marcar **"Add Python to PATH"** para poder usar pip desde cualquier terminal.

### 🟢 Instalación de Node.js

Descarga e instala Node.js desde [nodejs.org](https://nodejs.org/). Esto incluirá automáticamente **npm**.

### 🗺️ Instalación de Nmap

#### Windows:
```bash
# Descarga desde: https://nmap.org/download.html
# O usando chocolatey:
choco install nmap
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install nmap
```

#### macOS:
```bash
brew install nmap
```

### 📥 Clonar el Repositorio

#### Opción 1: Usando Git
```bash
git clone https://github.com/Pabloescobarxde/Stelarysv1.git
cd Stelarysv1
```

#### Opción 2: Descarga directa
- Descarga el ZIP del repositorio
- Pulsa **"Code"** → **"Download ZIP"**
- Extrae todos los contenidos

> [!CAUTION]
> **No ejecutes archivos desde dentro del ZIP**. El código necesita acceso a múltiples carpetas y archivos para funcionar correctamente.

### 📦 Instalación de Dependencias

#### Dependencias de Python:
```bash
pip install -r requirements.txt
```

#### Dependencias de Node.js:
```bash
npm install
```

> [!NOTE]
> Si aparecen errores de módulos faltantes, instálalos individualmente:
> ```bash
> pip install <nombre_del_modulo>
> npm install <nombre_del_paquete>
> ```

---

## 🔍 ¿Qué es Stelarys Tool?

<div align="center">

**Stelarys Tool** es una herramienta híbrida de pentesting especializada para **Minecraft** que combina la potencia de **Python**, **JavaScript/Node.js** y **Nmap** para ofrecer capacidades avanzadas de análisis de seguridad.

🎯 **Misión**: Proporcionar una suite completa para auditorías de seguridad y pentesting ético en servidores de Minecraft.

</div>

### ✨ Características Principales

- 🛡️ **Pentesting Avanzado**: Herramientas especializadas para Minecraft
- 🔍 **Análisis de Red**: Integración con Nmap para escaneo de puertos y servicios  
- 🐍 **Backend Python**: Procesamiento de datos y lógica principal
- 🟢 **Frontend Node.js**: Interfaz moderna y APIs RESTful
- 📊 **Reportes Detallados**: Análisis completos de vulnerabilidades
- 🎮 **Interfaz Intuitiva**: Fácil de usar para principiantes y expertos
- ⚡ **Alto Rendimiento**: Arquitectura optimizada para grandes servidores

### 🔧 Capacidades Técnicas

- **Escaneo de Puertos**: Detección de servicios activos
- **Análisis de Vulnerabilidades**: Identificación de puntos débiles
- **Monitoreo en Tiempo Real**: Supervisión continua de seguridad
- **Generación de Reportes**: Documentación automática de hallazgos
- **APIs REST**: Integración con otras herramientas

---

## 🚀 Uso

### 🎯 Ejecución Principal

```bash
# Usando Python
python stelarys.py

# Usando Python 3 explícitamente
python3 stelarys.py

# En Windows (archivo batch)
start.bat

# Usando Node.js
node app.js
```

### 📋 Comandos Básicos

```bash
# Escaneo básico
stelarys scan -t <target_ip>

# Análisis completo
stelarys audit -s <server_address>

# Generar reporte
stelarys report -o output.html
```

---

## 📜 Licencia

> [!NOTE]
> Al descargar, instalar o usar **Stelarys Tool**, aceptas automáticamente los términos y condiciones especificados en el archivo `LICENSE` de este repositorio.

---

## ⚠️ Nota Importante

> [!WARNING]  
> **⚖️ Descargo de Responsabilidad Legal**
> 
> - Este software fue desarrollado **exclusivamente con fines educativos** y de investigación en ciberseguridad
> - **No me hago responsable** de ningún daño, pérdida o consecuencia derivada del uso de esta herramienta
> - Es **responsabilidad del usuario** utilizar esta herramienta de manera ética y legal
> - **Solo debe usarse** en sistemas propios o con autorización explícita del propietario
> - El uso malintencionado de esta herramienta puede ser **ilegal** en tu jurisdicción

> [!CAUTION]
> **🎯 Uso Ético Únicamente**
> 
> Esta herramienta está diseñada para:
> - ✅ Auditorías de seguridad autorizadas
> - ✅ Pentesting ético en sistemas propios
> - ✅ Investigación académica y educativa
> - ✅ Mejora de la seguridad de servidores propios
> 
> **NO** debe usarse para:
> - ❌ Ataques no autorizados
> - ❌ Acceso ilegal a sistemas
> - ❌ Cualquier actividad maliciosa

---

## 🙏 Créditos

<div align="center">

### 👨‍💻 Desarrollador Principal
**[Pablito](https://github.com/Pabloescobarxde)** - *Creador y Desarrollador Principal*
> *Arquitectura del sistema, desarrollo del core, integración de tecnologías*

### 🤝 Colaboradores Especiales

**[@pepitogrillo05_term](https://github.com/pepitogrillo05_term)** - *Colaborador en Reestructuración*
> *Contribuciones en la optimización y reestructuración del código base*

### 🛠️ Tecnologías Utilizadas

Agradecimientos especiales a las comunidades de:
- **Python Software Foundation** por Python
- **Node.js Foundation** por Node.js  
- **Nmap Development Team** por Nmap
- **GitHub** por el hosting del repositorio

</div>

---

<div align="center">

**⭐ Si **Stelarys Tool** te resulta útil, no olvides darle una estrella ⭐**

[![GitHub stars](https://img.shields.io/github/stars/Pabloescobarxde/Stelarysv1.svg?style=social&label=Star)](https://github.com/Pabloescobarxde/Stelarysv1)
[![GitHub forks](https://img.shields.io/github/forks/Pabloescobarxde/Stelarysv1.svg?style=social&label=Fork)](https://github.com/Pabloescobarxde/Stelarysv1/fork)

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=Pabloescobarxde.Stelarysv1)

---

**🚀 ¡Únete a la comunidad de Stelarys Tool y ayuda a hacer el gaming más seguro! 🛡️**

</div>
