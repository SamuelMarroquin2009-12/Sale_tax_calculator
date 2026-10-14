"""
PLANTILLA DE CONFIGURACIÓN (esta SÍ se sube a GitHub).

Instrucciones de uso:
  1. Copia este archivo y llama la copia  secret_config.py
        Windows (cmd):   copy secret_config_sample.py secret_config.py
        Linux / macOS:   cp secret_config_sample.py secret_config.py
  2. Abre secret_config.py y reemplaza los valores de abajo con los datos
     de TU base de datos PostgreSQL de Render
     (Render -> tu base de datos -> pestaña "Connections" / "External Database URL").
  3. NUNCA subas secret_config.py a GitHub (ya está en .gitignore).
"""

DB_HOST = "dpg-xxxxxxxxxxxxxxxxxxxx-a.oregon-postgres.render.com"
DB_PORT = 5432
DB_NAME = "nombre_de_tu_base_de_datos"
DB_USER = "usuario_de_tu_base_de_datos"
DB_PASSWORD = "contraseña_de_tu_base_de_datos"
