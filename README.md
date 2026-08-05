# Simulador de Hipoteca Inversa

Se requiere una aplicación que calcule la cuota mensual que el banco pagaría a una persona que tome una hipoteca inversa, entregando su inmueble en garantía a cambio de una renta mensual durante un plazo pactado.

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

> **Nota:** el rango de 1 a 240 meses no corresponde a un límite legal fijado por el Decreto 1398 de 2020 (la norma colombiana no define un tope explícito de plazo), sino a un supuesto de trabajo definido con el experto entrevistado, basado en la práctica común del mercado de pactar rentas temporales en múltiplos de años (10, 15 o 20 años).

## Casos de prueba

El proyecto incluye 10 casos de prueba construidos a partir de la entrevista con el experto: 3 normales, 3 extraordinarios y 4 de error. Están documentados en el libro de Excel `casos_de_prueba.xlsx` y automatizados como pruebas unitarias en `Tests_Hipoteca_Inversa.py`.

## Requisitos

- Python 3.10 o superior
- `pytest` para ejecutar las pruebas unitarias (ver `requirements.txt`)

## Instalación

```bash
git clone https://github.com/Jose-Dv/Hipoteca-inversa
cd Hipoteca-inversa
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

El programa solicita el valor del inmueble, el porcentaje de desembolso, la tasa de interés mensual y el plazo en meses, y devuelve el valor efectivo, la cuota mensual, el total de abonos y el total de intereses, o el mensaje de error correspondiente si algún dato viola una regla de negocio.

## Pruebas

```bash
pytest Tests_Hipoteca_Inversa.py -v
```

Los 10 casos de prueba (3 normales, 3 extraordinarios, 4 de error) están automatizados y todos pasan exitosamente sobre la lógica implementada en `Logica_Hipoteca_Inversa.py`.

## Estructura del proyecto

El repositorio no usa carpetas: todos los archivos están en la raíz del proyecto.

```
Hipoteca-inversa/
├── Logica_Hipoteca_Inversa.py   # Lógica de negocio: cálculo de cuota, abonos, intereses y validaciones
├── Tests_Hipoteca_Inversa.py    # 10 casos de prueba automatizados (3 normales, 3 extraordinarios, 4 de error)
├── casos_de_prueba.xlsx         # Matriz de los 10 casos de prueba en Excel
├── requirements.txt             # Dependencias del proyecto (pytest)
└── README.md                    # Documentación del proyecto
```

## Metodología

1. Se realizó una entrevista grabada (audio) con un experto en hipoteca inversa para identificar variables de entrada, variables de salida y la fórmula de cálculo.
2. Con esa información se construyó el libro de Excel con los 10 casos de prueba (3 normales, 3 extraordinarios, 4 de error).
3. Se implementó la lógica de negocio en Python siguiendo exactamente la fórmula y las reglas de validación suministradas por el experto.
4. Se automatizaron los 10 casos de prueba como tests unitarios con `pytest` para verificar que el aplicativo cumple lo esperado.

## Autores

Sebastian Velasquez
...
Jose Diaz
