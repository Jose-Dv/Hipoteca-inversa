# Hipoteca Inversa

Aplicación de consola en Python para simular el cálculo de una **hipoteca inversa**, siguiendo principios de código limpio y arquitectura por capas (Modelo - Vista - Controlador).

## Integrantes del equipo
 
| Nombre | GitHub |
|---|---|
| Jhoan Rios | [@jhoan-rios](https://github.com/Jhoan-rios) |
| José Berrío | [@JoseBerrioC](https://github.com/JoseBerrioC) |
 

## Estructura del proyecto

```
Hipoteca-inversa/
├── assets/
│   └── icono.ico                     # Ícono de la aplicación de escritorio
├── doc/
│   ├── EntrevistaJuanDavid.mp3      # Entrevista de levantamiento de requisitos
│   └── casos_de_prueba.xlsx         # Casos de prueba documentados
├── src/
│   ├── controller/
│   │   └── __init__.py              # Orquesta la comunicación entre view y model
│   ├── model/
│   │   ├── __init__.py
│   │   └── logica_hipoteca_inversa.py  # Lógica de negocio y cálculos financieros
│   └── view/
│       ├── __init__.py
│       ├── console.py                # Interfaz de consola (entrada/salida de datos)
│       └── gui/
│           ├── __init__.py
│           └── hipoteca_inversa_gui.py  # Interfaz gráfica de escritorio (Kivy)
├── tests/
│   ├── __init__.py
│   └── tests_hipoteca_inversa.py    # Pruebas unitarias de la lógica de negocio
├── .gitignore
├── HipotecaInversa.spec              # Configuración de PyInstaller para generar el .exe
├── requirements.txt
├── LICENSE
└── README.md
```

### Descripción de la arquitectura

El proyecto sigue una separación de responsabilidades tipo **MVC**:

- **`model`**: contiene toda la lógica de cálculo de la hipoteca inversa (validaciones, fórmulas financieras, reglas de negocio y excepciones propias del dominio). No depende de cómo se muestren los datos.
- **`view`**: expone la interfaz de consola (`console.py`), encargada de solicitar datos al usuario y mostrar resultados. No contiene lógica de negocio.
- **`controller`**: actúa como intermediario entre `view` y `model`, coordinando el flujo de la aplicación sin mezclar responsabilidades de cálculo ni de presentación.
- **`tests`**: pruebas unitarias que validan el comportamiento de `model`, incluyendo casos válidos, casos límite y manejo de excepciones.
- **`doc`**: soporte documental del proyecto (entrevista de requisitos y casos de prueba).

## Funcionalidades

La lógica de negocio (`src/model/logica_hipoteca_inversa.py`) expone la función `desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)`, que calcula, usando la fórmula de anualidad financiera:

- **Cuota mensual**: el valor que el banco pagaría mensualmente al propietario.
- **Abonos totales**: la suma de todas las cuotas pagadas durante el plazo.
- **Intereses totales**: la diferencia entre los abonos totales y el valor financiado del inmueble.

Si la tasa mensual es `0`, el cálculo usa una división simple del valor financiado entre el número de meses, evitando la indeterminación de la fórmula de anualidad.

### Reglas de negocio y validaciones

La función valida los datos de entrada y lanza una excepción específica por cada regla incumplida:

| Excepción | Condición que la dispara |
|---|---|
| `ValorPropiedad0` | El valor del inmueble es menor o igual a 0 |
| `HipotecaUsura` | La tasa mensual supera el 4% (límite de usura) |
| `PlazoMayor240` | El plazo excede los 240 meses (20 años) |
| `PlazoMenorIgual0` | El plazo es menor o igual a 0 meses |

### Interfaz gráfica (GUI)
 
La GUI (`src/view/gui/hipoteca_inversa_gui.py`), construida con **Kivy**, ofrece:
 
- Formulario con los 4 campos de entrada (valor del inmueble, porcentaje de desembolso, tasa mensual, plazo).
- Validación de formato con resaltado visual del campo con error y mensajes descriptivos.
- Manejo de las excepciones de negocio del modelo, mostrando el motivo exacto del rechazo.
- Botón **Calcular** (también disponible con la tecla Enter) y botón **Limpiar** para reiniciar el formulario.
- Resultado detallado: monto del préstamo, cuota mensual, total de abonos y total de intereses.

### Pruebas unitarias

`tests/tests_hipoteca_inversa.py` valida el comportamiento de `desembolso_mensual` con:

- 3 casos normales con distintos valores de inmueble, porcentaje, tasa y plazo.
- 3 casos extraordinarios: tasa mensual en cero, desembolso único a 1 mes con 100% de financiación, y plazo máximo permitido (240 meses).
- 4 casos de error, uno por cada excepción de negocio (`ValorPropiedad0`, `HipotecaUsura`, `PlazoMenorIgual0`, `PlazoMayor240`).

## Ejecutar sin instalar Python (solo Windows)
 
Si solo quieres **usar la aplicación** sin instalar Python ni dependencias, descarga el ejecutable ya compilado:
 
1. Ve a la sección [**Releases**](https://github.com/Jhoan-rios/Hipoteca-inversa/releases) del repositorio.
2. Descarga el archivo `.zip` de la versión más reciente (ej. `HipotecaInversa-v1.0-Windows.zip`).
3. Descomprime el `.zip` completo en cualquier carpeta de tu equipo — **no muevas ni copies solo el `.exe` por separado**, necesita los archivos `.dll` que lo acompañan.
4. Haz doble clic en `HipotecaInversa.exe` dentro de la carpeta descomprimida.
No se requiere ninguna instalación adicional: el ejecutable ya incluye Python, Kivy y todas sus dependencias.
 
---

## Requisitos

- Python 3.10 o superior
- No se requieren dependencias externas (usa únicamente la librería estándar de Python)

Puedes verificar tu versión de Python con:

```bash
python --version
```

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/Jose-Dv/Hipoteca-inversa.git
```

### 2. Ubicarse en la carpeta del proyecto

```bash
cd Hipoteca-inversa
```

### 3. Ejecutar la interfaz de consola

```bash
python src/view/console.py
```

Esto iniciará la aplicación en modo consola, donde podrás ingresar los datos solicitados (valor del inmueble, porcentaje de financiación, tasa de interés mensual y plazo en meses) para obtener la cuota mensual, los abonos totales y los intereses totales de la hipoteca inversa.

### 4. Ejecutar las pruebas unitarias

Desde la raíz del proyecto:

```bash
python -m unittest tests/tests_hipoteca_inversa.py
```

O bien, si prefieres ejecutar todas las pruebas del proyecto automáticamente:

```bash
python -m unittest discover -s tests
```

Un resultado exitoso mostrará algo similar a:

```
----------------------------------------------------------------------
Ran 10 tests in 0.00Xs

OK
```
### 5. Generar el ejecutable de Windows
 
Con las dependencias instaladas (incluye `pyinstaller` en `requirements.txt`):
 
```bash
python -m PyInstaller HipotecaInversa.spec --clean
```
 
El ejecutable queda en `dist\HipotecaInversa\HipotecaInversa.exe`, junto con los `.dll` que necesita.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
