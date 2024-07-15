#!/bin/bash
# Actualizar los paquetes y instalar dependencias del sistema
apt-get update && apt-get install -y python3-dev build-essential
apt-get install -y curl apt-transport-https

# Añadir la clave y el repositorio de Microsoft para el controlador ODBC 17
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Actualizar los paquetes nuevamente y instalar el controlador ODBC 17
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Crear un entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Instalar dependencias de Python
pip install -r requirements.txt
