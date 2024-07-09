#!/usr/bin/env bash
# Instalar dependencias del sistema
apt-get update && apt-get install -y python3-dev build-essential

# Crear un entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Instalar dependencias de Python
pip install -r requirements.txt