# Simulador de Hipoteca Inversa

Aplicativo en Python que simula el cálculo de la cuota mensual que un banco le pagaría a una persona que constituye una **hipoteca inversa**, entregando su inmueble en garantía a cambio de una renta mensual durante un plazo pactado.

El proyecto surge de una entrevista con un experto en el tema (grabada en audio como evidencia académica), de la cual se extrajeron las variables de entrada, las variables de salida, la fórmula financiera y las reglas de negocio que rigen el cálculo.

## Descripción del problema

En una hipoteca inversa, el banco no le presta dinero a la persona para que ella pague cuotas, sino todo lo contrario: el banco le entrega una cuota mensual al propietario a cambio de quedarse con el derecho de cobro sobre el inmueble. El experto entrevistado precisó un punto clave: los bancos **no hipotecan el 100% del valor del inmueble**, sino solo un porcentaje de desembolso (similar al *Principal Limit Factor* usado en hipotecas inversas reales), para garantizar que puedan recuperar el capital entregado más los intereses causados durante todo el plazo.

## Variables de entrada

| Variable | Descripción | Restricción |
|---|---|---|
| Valor del inmueble | Valor comercial del inmueble | Debe ser mayor a 0 |
| % de desembolso | Porcentaje del valor del inmueble que el banco reconoce como base para hipotecar | Entre 0% y 100% |
| Tasa de interés mensual | Tasa pactada para el cálculo de la cuota | No puede superar el 4% mensual (tope de usura del ejercicio) |
| Plazo en meses | Duración de la renta periódica | Entre 1 y 240 meses |

## Variables de salida

- **Valor efectivo**: valor del inmueble multiplicado por el porcentaje de desembolso (base real sobre la que se calcula la cuota).
- **Cuota mensual**: dinero que el banco paga al propietario cada mes.
- **Total abonos**: suma de todas las cuotas mensuales durante el plazo.
- **Total intereses**: diferencia entre el total de abonos y el valor efectivo hipotecado.

## Fórmula utilizada

La cuota mensual se calcula con la fórmula de anualidad, aplicada de forma inversa a como se usa en un crédito tradicional:

```
Cuota = Valor_efectivo * i / (1 - (1 + i) ** -n)
```

Donde `i` es la tasa de interés mensual y `n` es el plazo en meses. Cuando la tasa es 0% (promociones de "tasa cero"), la cuota se calcula como el valor efectivo dividido entre el número de meses.

## Reglas de negocio (validaciones)

1. El valor del inmueble debe ser mayor que cero.
2. La tasa de interés mensual no puede superar el máximo de usura definido para el ejercicio (4% mensual).
3. El plazo en meses debe estar entre 1 y 240; valores en cero, negativos o mayores al límite se rechazan.

## Casos de prueba

El proyecto incluye 10 casos de prueba construidos a partir de la entrevista con el experto: 3 normales, 3 extraordinarios y 4 de error. Están documentados en el libro de Excel `casos_prueba_hipoteca_inversa.xlsx` y automatizados como pruebas unitarias en `tests/test_casos.py`.


## Requisitos

- Python 3.10 o superior
- `pytest` para ejecutar las pruebas unitarias (ver `requirements.txt`)

## Instalación

```bash
git clone https://github.com/usuario/simulador-hipoteca-inversa.git
cd simulador-hipoteca-inversa
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

El programa solicita el valor del inmueble, el porcentaje de desembolso, la tasa de interés mensual y el plazo en meses, y devuelve el valor efectivo, la cuota mensual, el total de abonos y el total de intereses, o el mensaje de error correspondiente si algún dato viola una regla de negocio.

## Pruebas

```bash
pytest tests/test_casos.py -v
```

Los 10 casos de prueba (3 normales, 3 extraordinarios, 4 de error) están automatizados y todos pasan exitosamente sobre la lógica implementada en `hipoteca_inversa.py`.

## Estructura del proyecto

```
simulador-hipoteca-inversa/
├── main.py                                  # Aplicativo de consola
├── hipoteca_inversa.py                      # Lógica de negocio y validaciones
├── tests/
│   └── test_casos.py                        # 10 casos de prueba automatizados
├── docs/
│   ├── guion_entrevista_hipoteca_inversa.md # Guion de la entrevista con el experto
│   └── casos_prueba_hipoteca_inversa.xlsx   # Matriz de casos de prueba en Excel
├── requirements.txt
└── README.md
```

## Metodología

1. Se realizó una entrevista grabada (audio) con un experto en hipoteca inversa para identificar variables de entrada, variables de salida y la fórmula de cálculo.
2. Con esa información se construyó el libro de Excel con los 10 casos de prueba (3 normales, 3 extraordinarios, 4 de error).
3. Se implementó la lógica de negocio en Python siguiendo exactamente la fórmula y las reglas de validación suministradas por el experto.
4. Se automatizaron los 10 casos de prueba como tests unitarios con `pytest` para verificar que el aplicativo cumple lo esperado.

## Autores

Sebastian Velasquez 
Jose Diaz
