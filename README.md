# Hipoteca Inversa

Aplicación en Python para simular el cálculo de una **hipoteca inversa**: la cuota mensual que el banco pagaría a una persona que toma una hipoteca inversa. Tiene interfaz de consola, interfaz gráfica con Kivy y una aplicación web hecha con Flask y Blueprints que guarda cada consulta en una base de datos PostgreSQL (Neon) y permite buscarlas por nombre. Sigue principios de código limpio y una arquitectura por capas (Modelo - Vista - Controlador).

**Aplicación publicada:** [https://hipoteca-inversa.onrender.com/](https://hipoteca-inversa.onrender.com/). Como usa el plan gratuito de Render, la primera carga después de un rato sin visitas puede tardar unos segundos.

## Entradas, proceso y salidas

### Entradas

| Dato | Qué es | Reglas |
|---|---|---|
| Valor del inmueble | Valor comercial de la propiedad | Mayor que 0 |
| Porcentaje a financiar | Parte del valor del inmueble que el banco desembolsa. En la web se escribe en porcentaje (por ejemplo `40`) | Número |
| Tasa de interés mensual | Interés que se cobra cada mes. En la web se escribe en porcentaje (por ejemplo `1.2`) | No puede superar el 4 % mensual (límite de usura) |
| Plazo en meses | Duración del desembolso | Entre 1 y 240 meses (20 años) |
| Nombre (solo en la web, opcional) | Etiqueta para encontrar la consulta después | Hasta 100 caracteres |

### Proceso

1. Se convierte el texto escrito en números (la web divide los porcentajes entre 100). Si algo no es un número, se muestra un mensaje de error.
2. Se validan las reglas de negocio: valor del inmueble mayor que 0, tasa mensual de máximo 4 % y plazo entre 1 y 240 meses.
3. Se calcula el monto del préstamo: `monto = valor del inmueble × porcentaje a financiar`.
4. Se calcula la cuota mensual con la fórmula de anualidad financiera: `cuota = monto × i / (1 − (1 + i)^−n)`, donde `i` es la tasa mensual y `n` el plazo en meses. Si la tasa es 0, `cuota = monto / n`.
5. Se calcula el total de abonos: `total de abonos = cuota × n`.
6. Se calcula el total de intereses: `total de intereses = total de abonos − monto`.
7. Solo en la web: la consulta se guarda en la base de datos con un identificador único (UUID) y se muestra el resultado.

### Salidas

- **Cuota mensual**: lo que el banco pagaría cada mes al propietario.
- **Total de abonos**: la suma de todas las cuotas del plazo.
- **Total de intereses**: la diferencia entre el total de abonos y el monto financiado.
- **Mensaje de error** cuando un dato no es válido (ver la tabla de mensajes en la guía de uso de la web).

### Ejemplo

Valor del inmueble `100.000.000`, porcentaje `14 %`, tasa `3,4 %` mensual y plazo de `30` meses:

- Monto financiado: 14.000.000
- Cuota mensual: 751.691,60
- Total de abonos: 22.550.748,02
- Total de intereses: 8.550.748,02

## Estructura del proyecto

```
Hipoteca-inversa/
├── doc/
│   ├── EntrevistaJuanDavid.mp3      # Entrevista de levantamiento de requisitos
│   └── CasosPrueba.xlsx             # Casos de prueba documentados
├── src/
│   ├── controller/
│   │   ├── __init__.py
│   │   ├── hipoteca_controller.py   # Parseo de datos y manejo de errores del cálculo
│   │   └── consultas_controller.py  # Crear/borrar tabla, insertar, buscar y eliminar consultas
│   ├── model/
│   │   ├── __init__.py
│   │   ├── logica_hipoteca_inversa.py  # Lógica de negocio y cálculos financieros
│   │   └── consulta.py              # Clase Consulta (una fila de la tabla consultas)
│   └── view/
│       ├── __init__.py
│       ├── console.py               # Interfaz de consola
│       ├── interfaz_kivy.py         # Interfaz gráfica con Kivy
│       └── web/
│           ├── __init__.py
│           └── vista_hipoteca.py    # Blueprint de Flask con las rutas de la web
├── static/
│   └── css/
│       └── estilos.css              # Estilos de la web
├── templates/
│   ├── index.html                   # Inicio: formulario de cálculo
│   ├── resultado.html               # Consulta guardada con su información
│   └── consultas.html               # Historial, búsqueda y borrado
├── tests/
│   ├── __init__.py
│   ├── tests_hipoteca_inversa.py    # Pruebas unitarias de la lógica de cálculo
│   └── tests_consultas_controller.py  # Pruebas de insertar, buscar y eliminar (con BD)
├── app.py                           # Arranca la web y registra el Blueprint
├── .gitignore
├── .python-version                  # Versión de Python que usa Render (3.12)
├── LICENSE
├── requirements.txt                 # psycopg2-binary, Flask y gunicorn
├── requirements-kivy.txt            # Lo anterior + Kivy (solo para la interfaz gráfica)
├── secret_config_sample.py          # Plantilla de la configuración de la BD
└── README.md
```

### Descripción de la arquitectura

- **`model`**: `logica_hipoteca_inversa.py` contiene la lógica de cálculo (validaciones, fórmulas financieras, reglas de negocio y excepciones propias). `consulta.py` define la clase `Consulta`: los datos ingresados, el resultado, el nombre opcional y un `id` único (UUID) que se genera al crear la consulta. Ninguno depende de cómo se muestren los datos.
- **`view`**: la consola (`console.py`), la interfaz gráfica (`interfaz_kivy.py`) y la web (`web/vista_hipoteca.py` con las plantillas de `templates/` y los estilos de `static/css/`). Ninguna contiene lógica de negocio.
  - La web usa un **Blueprint de Flask** llamado `vista`, que reúne las rutas de la aplicación. `app.py`, en la raíz, solo crea la aplicación Flask y registra ese Blueprint; Flask y los servidores de publicación esperan encontrar `app.py` en la raíz.
- **`controller`**: intermediario entre las vistas y el modelo o la base de datos.
  - `hipoteca_controller.py` convierte el texto ingresado en los tipos del modelo (tolerando formatos como `1,2` o `300.000.000`) y traduce cualquier error a un mensaje legible mediante `ErrorCalculoHipoteca`. Lo usan la consola y Kivy.
  - `consultas_controller.py` es el único que habla con PostgreSQL (con `psycopg2`). Expone `crear_tabla`, `borrar_tabla`, `insertar`, `buscar` y `eliminar`. La tabla se crea sola: `insertar` y `buscar` ejecutan `CREATE TABLE IF NOT EXISTS` antes de trabajar, así que no hay que crearla a mano. Para conectarse usa `secret_config.py` si existe (en local) y, si no, las variables de entorno `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y `PGPORT` (en el servidor).
- **`tests`**: pruebas unitarias del cálculo y de la base de datos.

## Funcionalidades

### Cálculo de la hipoteca inversa

La función `desembolso_mensual(parametros)` de `src/model/logica_hipoteca_inversa.py` calcula, con la fórmula de anualidad financiera:

- **Cuota mensual**: el valor que el banco pagaría mensualmente al propietario.
- **Abonos totales**: la suma de todas las cuotas pagadas durante el plazo.
- **Intereses totales**: la diferencia entre los abonos totales y el valor financiado.

Si la tasa mensual es `0`, el cálculo divide el valor financiado entre el número de meses.

| Excepción | Condición que la dispara |
|---|---|
| `ValorPropiedadCero` | El valor del inmueble es menor o igual a 0 |
| `HipotecaUsura` | La tasa mensual supera el 4% (límite de usura) |
| `PlazoMayorPermitido` | El plazo excede los 240 meses (20 años) |
| `PlazoMenorIgualCero` | El plazo es menor o igual a 0 meses |

### Aplicación web

Las rutas están en `src/view/web/vista_hipoteca.py`. En local, la aplicación queda en `http://127.0.0.1:5000`:

- **Inicio (`/`)**: menú principal con el formulario (valor del inmueble, porcentaje a financiar en %, tasa de interés mensual en %, plazo en meses y nombre opcional) y el enlace **Ver consultas**.
- **Resultado (`/calcular_cuota`)**: al calcular, la consulta (datos y resultado) se guarda en la base de datos y se muestra "Consulta guardada exitosamente" con toda la información.
- **Consultas (`/consultas`)**: historial de todas las consultas guardadas, de la más reciente a la más antigua, con una barra de búsqueda por nombre y un botón **Eliminar** en cada fila (`/eliminar_consulta/<id>`), que pide confirmación.
- **Borrar tabla (`/borrar_tabla`)**: al final de la página de consultas, en la "Zona peligrosa". Elimina todas las consultas, y solo actúa si el usuario escribe la palabra `BORRAR`.

No hay que crear las tablas a mano: si no existen, se crean solas en la primera consulta o búsqueda, también después de usar **Borrar tabla**.

Cada consulta se identifica con un UUID generado en Python (`uuid.uuid4()`), guardado como texto en la columna `id`. No se usa un contador autoincremental de la base de datos.

### Pruebas

- `tests/tests_hipoteca_inversa.py`: 3 casos normales, 3 extraordinarios (tasa cero, desembolso único a 1 mes, plazo máximo) y 4 de error, uno por excepción.
- `tests/tests_consultas_controller.py`: 6 casos contra la base de datos (insertar con nombre, insertar sin nombre, buscar por parte del nombre, buscar un nombre inexistente, crear la tabla cuando no existe y eliminar una consulta). Su fixture (`setUpClass`) borra y vuelve a crear la tabla `consultas` una sola vez al inicio.

## Requisitos

- Python 3.10 o superior
- Una base de datos PostgreSQL (por ejemplo, un proyecto gratuito en [Neon](https://neon.com))
- Paquetes de Python (consola, web, base de datos y pruebas):

  ```bash
  pip install -r requirements.txt
  ```

- Solo si va a usar la interfaz gráfica (Kivy), instale en cambio:

  ```bash
  pip install -r requirements-kivy.txt
  ```

## Configuración de la base de datos

1. Cree una base de datos PostgreSQL vacía (en Neon, desde el botón **Connect** de la consola se copian el host, la base, el usuario y la contraseña).
2. Copie `secret_config_sample.py` como `secret_config.py` (en la raíz del proyecto) y escriba allí el host, el nombre de la base, el usuario, la contraseña y el puerto. `secret_config.py` está en `.gitignore`: **no lo suba a GitHub**.

   ```bash
   cp secret_config_sample.py secret_config.py
   ```

3. En un servidor donde no existe `secret_config.py` (como Render), la aplicación lee los mismos datos de las variables de entorno `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y, opcionalmente, `PGPORT` (por defecto 5432).

> ⚠️ **Cuidado:** las pruebas de `tests_consultas_controller.py` **borran y recrean** la tabla `consultas`, perdiendo sus datos. Úselas con una base de desarrollo.

> Si su base ya tenía una tabla `consultas` de una versión anterior (con `id` numérico), bórrela una vez: `CREATE TABLE IF NOT EXISTS` no cambia una tabla que ya existe.

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/Jose-Dv/Hipoteca-inversa.git
cd Hipoteca-inversa
```

Luego instale las dependencias y configure la base de datos como se explica arriba.

### 2. Interfaz de consola

```bash
python src/view/console.py
```

Pide el valor del inmueble, el porcentaje de desembolso, la tasa de interés mensual y el plazo en meses, y muestra la cuota mensual, los abonos totales y los intereses totales. No requiere base de datos.

### 3. Interfaz gráfica (Kivy)

Instale primero `requirements-kivy.txt` y, desde la raíz del proyecto, ejecute:

```bash
python -m src.view.interfaz_kivy
```

Se abre una ventana con los mismos campos y el botón **Calcular**. Los errores se muestran en la misma ventana. No requiere base de datos.

### 4. Aplicación web en local (con una base de datos en blanco)

1. Tenga instalado Python 3.10 o superior y una base de datos PostgreSQL vacía (por ejemplo, un proyecto de Neon).
2. Abra una terminal en la carpeta del proyecto y cree un entorno virtual:

   ```bash
   python -m venv .venv
   ```

3. Actívelo. En Windows:

   ```bash
   .venv\Scripts\activate
   ```

   En Linux o macOS:

   ```bash
   source .venv/bin/activate
   ```

4. Instale las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

5. Cree su archivo de configuración copiando la plantilla. En Windows:

   ```bash
   copy secret_config_sample.py secret_config.py
   ```

   En Linux o macOS:

   ```bash
   cp secret_config_sample.py secret_config.py
   ```

6. Abra `secret_config.py` y reemplace los valores de ejemplo por el host, la base, el usuario, la contraseña y el puerto de su base de datos.
7. Inicie la aplicación desde la raíz del proyecto:

   ```bash
   python app.py
   ```

8. Abra `http://127.0.0.1:5000` en el navegador. Para detener el servidor, presione `Ctrl + C` en la terminal.
9. No necesita crear las tablas: la primera vez que se guarda o se busca una consulta, la tabla `consultas` se crea sola.

El uso de cada pantalla se explica en la guía de uso de la aplicación web.

### 5. Ejecutar las pruebas unitarias

Desde la raíz del proyecto (con `secret_config.py` configurado):

```bash
python -m unittest discover -s tests -v
```

Un resultado exitoso termina con algo similar a:

```
----------------------------------------------------------------------
Ran 16 tests in 0.0XXs

OK
```

Para ejecutar solo las pruebas del cálculo (no requieren base de datos):

```bash
python -m unittest tests/tests_hipoteca_inversa.py
```

### 6. Publicar la web en Render

1. En Neon, abra la rama que usará la web publicada (por ejemplo `production`), pulse **Connect**, desactive *Connection pooling* y copie el host, la base, el usuario y la contraseña.
2. En Render, cree un **Web Service** conectado a este repositorio, rama `main`.
3. Configure: *Build Command* `pip install -r requirements.txt`, *Start Command* `gunicorn app:app` (también sirve `flask run -p 10000 -h 0.0.0.0`) y el tipo de instancia **Free**.
4. En *Environment Variables* agregue `PGHOST`, `PGDATABASE`, `PGUSER` y `PGPASSWORD` con los datos de Neon (y `PGPORT` solo si no usa el 5432).
5. Pulse **Deploy**. La dirección pública de la aplicación aparece en el panel del servicio.

Render usa el archivo `.python-version` para elegir la versión de Python. No suba nunca la contraseña al repositorio: va solo en las variables de entorno de Render.

La aplicación de este proyecto está publicada en [https://hipoteca-inversa.onrender.com/](https://hipoteca-inversa.onrender.com/).

## Guía de uso de la aplicación web

La aplicación se usa igual en la web publicada y en local; solo cambia la dirección con la que se abre.

### Dónde abrirla

| Modo | Dirección | Qué hace falta |
|---|---|---|
| Web publicada (Render) | [https://hipoteca-inversa.onrender.com/](https://hipoteca-inversa.onrender.com/) | Solo un navegador. La primera carga puede tardar unos segundos mientras el servicio despierta |
| En local | `http://127.0.0.1:5000` | Haber seguido el paso 4 de "Cómo ejecutar el proyecto" y tener el servidor corriendo |

### Paso a paso

1. **Calcular una consulta.** En la página de inicio escriba el valor del inmueble, el porcentaje a financiar (por ejemplo `40`), la tasa de interés mensual (por ejemplo `1.2`), el plazo en meses y, si quiere, un nombre. Pulse **Calcular**.
2. **Ver el resultado.** Aparece "Consulta guardada exitosamente" con los datos ingresados, la cuota mensual, el total de abonos y el total de intereses. Desde ahí puede hacer una **Nueva consulta** o ir a **Ver consultas**.
3. **Revisar el historial.** **Ver consultas** muestra una tabla con todas las consultas guardadas, de la más reciente a la más antigua.
4. **Buscar.** Escriba parte del nombre en la barra de búsqueda y pulse **Buscar**. No distingue mayúsculas de minúsculas. Con la barra vacía se muestran todas.
5. **Eliminar una consulta.** Pulse **Eliminar** en la fila que quiera quitar y acepte la confirmación. Las demás no se tocan.
6. **Borrar toda la tabla.** Al final de la página, en la "Zona peligrosa", escriba `BORRAR` y pulse **Borrar tabla**. Se eliminan todas las consultas; la tabla se vuelve a crear vacía sola.

### Mensajes de error

| Mensaje | Causa | Qué hacer |
|---|---|---|
| "Ingrese solo números en todos los campos" | Un campo tiene texto o está en un formato que no es número | Corregir el campo y volver a calcular |
| "el valor del inmueble debe ser mayor que cero" | El valor es 0 o negativo | Escribir un valor positivo |
| "la tasa mensual supera el máximo permitido (4%)" | La tasa mensual es mayor que el 4 % | Escribir una tasa de 4 o menos |
| "el plazo no debe ser mayor a 240 meses" | El plazo excede los 20 años | Escribir un plazo de 240 o menos |
| "el plazo debe estar entre 1 y 240 meses" | El plazo es 0 o negativo | Escribir un plazo de 1 a 240 |
| "Error inesperado" | Normalmente, un problema con la base de datos (conexión o configuración) | En local, revisar `secret_config.py`; en Render, revisar las variables de entorno |

### Tenga en cuenta

- **Los datos son compartidos.** La aplicación no tiene usuarios: todas las personas que abran la misma dirección ven, buscan y pueden eliminar las mismas consultas. No escriba datos personales reales.
- **Cada instalación local ve su propia base.** En local, las consultas que ve dependen de la base configurada en `secret_config.py`.

## Autores

Autores originales del proyecto:

- **Sebastian Velasquez**
- **Jose Diaz**

Aporte posterior:

- **Pedro Hernandez**: interfaz gráfica con Kivy (`src/view/interfaz_kivy.py`) y el controlador compartido entre las vistas (`src/controller/hipoteca_controller.py`).

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
