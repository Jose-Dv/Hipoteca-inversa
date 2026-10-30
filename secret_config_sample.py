"""Plantilla de configuración de la conexión a PostgreSQL (por ejemplo, Neon).

Instrucciones de uso:
1. Copie este archivo y guárdelo como ``secret_config.py`` en la raíz del
   proyecto (junto a este archivo).
2. Reemplace los valores de ejemplo por sus cadenas de conexión reales. En Neon:
   botón Connect de la consola, elija la rama, active Show Password y copie la
   cadena. Para PostgreSQL local use:
   ``postgresql://postgres:su_clave@localhost:5432/hipoteca_inversa``
3. NO suba ``secret_config.py`` a GitHub: contiene su contraseña. Ya está
   incluido en ``.gitignore``. Solo este archivo de ejemplo se versiona.
"""

# Base de datos que usa la aplicación (consola, Kivy y web).
DATABASE_URL = "postgresql://USUARIO:CONTRASENA@HOST/NOMBRE_BD?sslmode=require"

# Base de datos exclusiva para las pruebas: SIEMPRE distinta de DATABASE_URL,
# porque las pruebas borran y recrean las tablas. En Neon use otra rama.
DATABASE_URL_PRUEBAS = "postgresql://USUARIO:CONTRASENA@HOST/NOMBRE_BD_PRUEBAS?sslmode=require"
