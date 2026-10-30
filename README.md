# Hipoteca Inversa

Aplicación en Python para simular el cálculo de una **hipoteca inversa**: la cuota mensual que el banco pagaría a una persona que toma una hipoteca inversa. Tiene interfaz de consola, interfaz gráfica con Kivy y una aplicación web que guarda cada consulta en una base de datos PostgreSQL (Neon) y permite buscarlas por nombre. Sigue principios de código limpio y una arquitectura por capas (Modelo - Vista - Controlador).

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
│   │   └── consultas_controller.py  # Crear/borrar tabla, insertar y buscar consultas
│   ├── model/
│   │   ├── __init__.py
│   │   ├── logica_hipoteca_inversa.py  # Lógica de negocio y cálculos financieros
│   │   └── consulta.py              # Clase Consulta (una fila de la tabla consultas)
│   └── view/
│       ├── __init__.py
│       ├── console.py               # Interfaz de consola
│       └── interfaz_kivy.py         # Interfaz gráfica con Kivy
├── templates/
│   └── index.html                   # Página web: formulario, búsqueda e historial
├── tests/
│   ├── __init__.py
│   ├── tests_hipoteca_inversa.py    # Pruebas unitarias de la lógica de cálculo
│   └── tests_consultas_controller.py  # Pruebas de insertar y buscar (con BD)
├── app.py                           # Servidor local de la aplicación web
├── .gitignore
├── LICENSE
├── requirements.txt                 # psycopg2-binary, Flask y Kivy
├── secret_config_sample.py          # Plantilla de la configuración de la BD
└── README.md
```

### Descripción de la arquitectura

- **`model`**: `logica_hipoteca_inversa.py` contiene la lógica de cálculo (validaciones, fórmulas financieras, reglas de negocio y excepciones propias). `consulta.py` define la clase `Consulta`: los datos ingresados, el resultado y el nombre opcional. Ninguno depende de cómo se muestren los datos.
- **`view`**: la consola (`console.py`), la interfaz gráfica (`interfaz_kivy.py`) y la web (`app.py` con `templates/index.html`). Ninguna contiene lógica de negocio.
- **`controller`**: intermediario entre las vistas y el modelo o la base de datos.
  - `hipoteca_controller.py` convierte el texto ingresado en los tipos del modelo (tolerando formatos como `1,2` o `300.000.000`) y traduce cualquier error a un mensaje legible mediante `ErrorCalculoHipoteca`. Lo usan la consola y Kivy.
  - `consultas_controller.py` es el único que habla con PostgreSQL (con `psycopg2`). Expone `crear_tabla`, `borrar_tabla`, `insertar` y `buscar`. La tabla se crea sola si no existe.
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

En `http://127.0.0.1:5000` hay un formulario con el valor del inmueble, el porcentaje a financiar (%), la tasa de interés mensual (%), el plazo en meses y un nombre opcional. Al calcular, la consulta (datos y resultado) se guarda en la base de datos. Debajo del formulario hay un historial con una barra de búsqueda por nombre.

No hay que crear las tablas a mano: si no existen, se crean en la primera consulta.

### Pruebas

- `tests/tests_hipoteca_inversa.py`: 3 casos normales, 3 extraordinarios (tasa cero, desembolso único a 1 mes, plazo máximo) y 4 de error, uno por excepción.
- `tests/tests_consultas_controller.py`: 5 casos contra la base de datos (insertar con nombre, insertar sin nombre, buscar por parte del nombre, buscar un nombre inexistente y crear la tabla cuando no existe). Su fixture (`setUpClass`) borra y vuelve a crear la tabla `consultas` una sola vez al inicio.

## Requisitos

- Python 3.10 o superior
- Una base de datos PostgreSQL (por ejemplo, un proyecto gratuito en [Neon](https://neon.com))
- Paquetes de Python:

  ```bash
  pip install -r requirements.txt
  ```

## Configuración de la base de datos

1. Cree una base de datos PostgreSQL vacía (en Neon, desde el botón **Connect** de la consola se copian el host, la base, el usuario y la contraseña).
2. Copie `secret_config_sample.py` como `secret_config.py` (en la raíz del proyecto) y escriba allí el host, el nombre de la base, el usuario, la contraseña y el puerto. `secret_config.py` está en `.gitignore`: **no lo suba a GitHub**.

   ```bash
   cp secret_config_sample.py secret_config.py
   ```

> ⚠️ **Cuidado:** las pruebas de `tests_consultas_controller.py` **borran y recrean** la tabla `consultas`, perdiendo sus datos. Úselas con una base de desarrollo.

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

Desde la raíz del proyecto:

```bash
python -m src.view.interfaz_kivy
```

Se abre una ventana con los mismos campos y el botón **Calcular**. Los errores se muestran en la misma ventana. No requiere base de datos.

### 4. Aplicación web

Con `secret_config.py` configurado, desde la raíz del proyecto:

```bash
python app.py
```

Abra `http://127.0.0.1:5000` en el navegador. Con una base de datos en blanco no hace falta ningún paso adicional: la tabla se crea en la primera consulta.

### 5. Ejecutar las pruebas unitarias

Desde la raíz del proyecto (con `secret_config.py` configurado):

```bash
python -m unittest discover -s tests -v
```

Un resultado exitoso termina con algo similar a:

```
----------------------------------------------------------------------
Ran 15 tests in 0.0XXs

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
