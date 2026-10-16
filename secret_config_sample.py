"""Plantilla de configuración de la conexión a PostgreSQL.

Instrucciones de uso:
1. Copie este archivo y guárdelo como ``secret_config.py`` en la raíz del
   proyecto (junto a este archivo).
2. Reemplace los valores de ejemplo por los datos reales de su base de datos.
3. NO suba ``secret_config.py`` a GitHub: contiene su contraseña. Ya está
   incluido en ``.gitignore``. Solo este archivo de ejemplo se versiona.
"""

PGHOST = 'PONGA EL HOST DE LA BD AQUI'          # ejemplo: localhost
PGDATABASE = 'PONGA EL NOMBRE DE LA BD AQUI'    # ejemplo: hipoteca_inversa
PGUSER = 'PONGA EL USUARIO AQUI'                # ejemplo: postgres
PGPASSWORD = 'PONGA LA CONTRASEÑA AQUI'
PGPORT = 5432
