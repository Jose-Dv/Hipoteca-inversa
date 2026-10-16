# Hipoteca Inversa

Aplicación en Python para simular el cálculo de una **hipoteca inversa** y para **registrar y buscar clientes** en una base de datos PostgreSQL, siguiendo principios de código limpio y arquitectura por capas (Modelo - Vista - Controlador). Tiene interfaz de consola y una interfaz gráfica con Kivy.

## Estructura del proyecto

```
Hipoteca-inversa/
├── doc/
│   ├── EntrevistaJuanDavid.mp3      # Entrevista de levantamiento de requisitos
│   └── CasosPrueba.xlsx             # Casos de prueba documentados
├── sql/
│   ├── crear-clientes.sql           # Scripts de creación de tablas (PostgreSQL)
│   ├── crear-hipotecas.sql
│   ├── crear-solicitudes.sql
│   ├── crear-usuarios.sql
│   ├── crear-viviendas.sql
│   └── insertar-datos-prueba.sql    # Datos de ejemplo (opcional)
├── src/
│   ├── controller/
│   │   ├── __init__.py
│   │   ├── hipoteca_controller.py   # Parseo de datos y manejo de errores del cálculo
│   │   └── cliente_controller.py    # Crear/borrar tablas, insertar y buscar clientes
│   ├── model/
│   │   ├── __init__.py
│   │   ├── logica_hipoteca_inversa.py  # Lógica de negocio y cálculos financieros
│   │   └── cliente.py               # Clase Cliente (entidad de la tabla clientes)
│   └── view/
│       ├── __init__.py
│       ├── console.py               # Interfaz de consola (menú)
│       └── interfaz_kivy.py         # Interfaz gráfica con Kivy (3 pestañas)
├── tests/
│   ├── __init__.py
│   ├── tests_hipoteca_inversa.py    # Pruebas unitarias de la lógica de cálculo
│   └── tests_cliente_controller.py  # Pruebas de insertar y buscar clientes (con BD)
├── .gitignore
├── LICENSE
├── requirements.txt                 # psycopg2-binary (BD) y Kivy (interfaz gráfica)
├── secret_config_sample.py          # Plantilla de la configuración de la BD
└── README.md
```

### Descripción de la arquitectura

El proyecto sigue una separación de responsabilidades tipo **MVC**:

- **`model`**: `logica_hipoteca_inversa.py` contiene la lógica de cálculo de la hipoteca inversa (validaciones, fórmulas financieras, reglas de negocio y excepciones propias del dominio). `cliente.py` define la clase `Cliente`, que representa una fila de la tabla `clientes`. Ninguno depende de cómo se muestren los datos.
- **`view`**: expone la interfaz de consola (`console.py`) y una interfaz gráfica construida con [Kivy](https://kivy.org/) (`interfaz_kivy.py`). Ambas ofrecen calcular una hipoteca, registrar un cliente y buscar clientes. Ninguna contiene lógica de negocio.
- **`controller`**: intermediario entre `view` y `model`/base de datos.
  - `hipoteca_controller.py` convierte el texto ingresado en los tipos del modelo (tolerando formatos como `1,2` o `300.000.000`) y traduce cualquier error a un mensaje legible mediante `ErrorCalculoHipoteca`.
  - `cliente_controller.py` valida los datos del cliente, accede a PostgreSQL (con `psycopg2`) y expone `crear_tablas`, `borrar_tablas`, `insertar_cliente`, `buscar_cliente_por_cedula` y `buscar_clientes`. Cualquier problema se informa con `ErrorCliente`.
- **`tests`**: pruebas unitarias del cálculo y de insertar/buscar clientes.
- **`sql`**: scripts para crear las tablas y datos de prueba.
- **`doc`**: soporte documental del proyecto (entrevista de requisitos y casos de prueba).

## Funcionalidades

### Cálculo de la hipoteca inversa

La lógica de negocio (`src/model/logica_hipoteca_inversa.py`) expone la función `desembolso_mensual(parametros)`, que calcula, usando la fórmula de anualidad financiera:

- **Cuota mensual**: el valor que el banco pagaría mensualmente al propietario.
- **Abonos totales**: la suma de todas las cuotas pagadas durante el plazo.
- **Intereses totales**: la diferencia entre los abonos totales y el valor financiado del inmueble.

Si la tasa mensual es `0`, el cálculo usa una división simple del valor financiado entre el número de meses, evitando la indeterminación de la fórmula de anualidad.

#### Reglas de negocio y validaciones

| Excepción | Condición que la dispara |
|---|---|
| `ValorPropiedadCero` | El valor del inmueble es menor o igual a 0 |
| `HipotecaUsura` | La tasa mensual supera el 4% (límite de usura) |
| `PlazoMayorPermitido` | El plazo excede los 240 meses (20 años) |
| `PlazoMenorIgualCero` | El plazo es menor o igual a 0 meses |

### Gestión de clientes

Los clientes se guardan en la tabla `clientes` de PostgreSQL:

| Campo | Regla |
|---|---|
| Cédula | Obligatoria, solo números (máx. 20) y única |
| Nombres / Apellidos | Obligatorios (máx. 100 caracteres) |
| Fecha de nacimiento | Opcional, formato `AAAA-MM-DD`, no puede ser futura |
| Teléfono / Dirección | Opcionales |

- **Insertar**: registra un cliente nuevo; si la cédula ya existe, muestra un mensaje de error.
- **Buscar**: por cédula exacta, o por parte del nombre o apellido (sin distinguir mayúsculas).

### Pruebas

- `tests/tests_hipoteca_inversa.py` valida `desembolso_mensual` con 3 casos normales, 3 casos extraordinarios (tasa cero, desembolso único a 1 mes, plazo máximo) y 4 casos de error, uno por excepción de negocio.
- `tests/tests_cliente_controller.py` contiene 5 casos de insertar y buscar contra la base de datos (insertar válido, insertar y buscar por cédula, cédula inexistente, cédula duplicada y búsqueda por nombre/apellido) y 4 validaciones de formato que no necesitan base de datos. Su *fixture* (`setUp`) borra y vuelve a crear las tablas antes de cada prueba.

## Requisitos

- Python 3.10 o superior
- PostgreSQL y sus datos de acceso (servidor, nombre de la base de datos, usuario y contraseña)
- Paquetes de Python (incluye `psycopg2-binary` y, para la interfaz gráfica, [Kivy](https://kivy.org/)):

  ```bash
  pip install -r requirements.txt
  ```

Puede verificar su versión de Python con:

```bash
python --version
```

## Configuración de la base de datos

1. **Cree una base de datos vacía** en PostgreSQL (por ejemplo, con `psql`):

   ```sql
   CREATE DATABASE hipoteca_inversa;
   ```

2. **Configure la conexión**: copie `secret_config_sample.py` como `secret_config.py` (en la raíz del proyecto) y escriba allí el host, el nombre de la base de datos, el usuario, la contraseña y el puerto. `secret_config.py` está en `.gitignore`: **no lo suba a GitHub**.

   ```bash
   cp secret_config_sample.py secret_config.py
   ```

3. **Cree las tablas**: antes de ejecutar la aplicación por primera vez, corra las pruebas unitarias (ver [paso 5](#5-ejecutar-las-pruebas-unitarias)); su fixture crea las tablas con los scripts de la carpeta `sql/`. Si prefiere hacerlo a mano, ejecute los archivos `sql/crear-*.sql` en su base de datos.

> ⚠️ **Cuidado:** las pruebas de `tests_cliente_controller.py` **borran y recrean** las tablas, perdiendo los datos que tengan. Úselas con una base de datos de desarrollo. Después de correrlas, las tablas quedan creadas y vacías.

4. *(Opcional)* Para cargar datos de ejemplo: ejecute `sql/insertar-datos-prueba.sql` en su base de datos.

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/Jose-Dv/Hipoteca-inversa.git
```

### 2. Ubicarse en la carpeta del proyecto

```bash
cd Hipoteca-inversa
```

Luego instale las dependencias y configure la base de datos como se explica arriba.

### 3. Ejecutar la interfaz de consola

```bash
python src/view/console.py
```

Se muestra un menú:

1. **Calcular hipoteca**: pide el valor del inmueble, el porcentaje de financiación, la tasa de interés mensual y el plazo en meses, y muestra la cuota mensual, los abonos totales y los intereses totales.
2. **Registrar cliente**: pide cédula, nombres, apellidos y, opcionalmente, fecha de nacimiento, teléfono y dirección, y los guarda en la base de datos.
3. **Buscar cliente**: busque escribiendo una cédula (solo números) o parte de un nombre o apellido.
4. **Salir**.

La opción 1 funciona sin base de datos; las opciones 2 y 3 requieren la base de datos configurada.

### 4. Ejecutar la interfaz gráfica (Kivy)

Desde la raíz del proyecto:

```bash
python -m src.view.interfaz_kivy
```

Se abre una ventana con tres pestañas:

- **Calcular hipoteca**: campos del cálculo y botón **Calcular**.
- **Registrar cliente**: formulario con botón **Guardar cliente**.
- **Buscar cliente**: búsqueda por cédula o por nombre/apellido.

Los errores (datos inválidos, cédula repetida, base de datos no disponible) se muestran en la misma ventana.

### 5. Ejecutar las pruebas unitarias

Desde la raíz del proyecto (con `secret_config.py` configurado):

```bash
python -m unittest discover -s tests -v
```

Un resultado exitoso termina con algo similar a:

```
----------------------------------------------------------------------
Ran 19 tests in 0.0XXs

OK
```

Para ejecutar solo las pruebas del cálculo (no requieren base de datos):

```bash
python -m unittest tests/tests_hipoteca_inversa.py
```

## Autores

- **Pedro Hernandez**: interfaz gráfica con Kivy (`src/view/interfaz_kivy.py`) y el controlador compartido entre las vistas (`src/controller/hipoteca_controller.py`).

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
