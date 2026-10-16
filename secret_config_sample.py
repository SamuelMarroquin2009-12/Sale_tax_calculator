# INSTRUCCIONES DE USO
#
# 1. Copie este archivo en la misma carpeta (junto al README) y llame la copia: secret_config.py
#       Windows:        copy secret_config_sample.py secret_config.py
#       Linux / macOS:  cp secret_config_sample.py secret_config.py
#
# 2. Abra secret_config.py y reemplace los valores de abajo con los datos de SU base de datos
#    PostgreSQL.
#       neon.tech: Dashboard -> "Connection Details" (Host, Database, User, Password)
#       Render:    su base de datos -> seccion "Connections" -> datos "External"
#
# 3. NUNCA suba secret_config.py a GitHub (ya esta en el .gitignore).
#    Solo este archivo de muestra (secret_config_sample.py) va en el repositorio.

PGHOST = 'PONGA EL HOST DE LA BD AQUI'          # el Host de su servidor (en Render, el Hostname EXTERNAL: termina en .render.com)
PGDATABASE = 'PONGA EL NOMBRE DE LA BD AQUI'
PGUSER = 'PONGA EL USUARIO AQUI'
PGPASSWORD = 'PONGA LA CONTRASEÑA AQUI'
PGPORT = 5432
