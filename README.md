# Simulador de Hipoteca Inversa

Se requiere una aplicación que calcule la cuota mensual que el banco pagaría a una persona que tome una hipoteca inversa, entregando su inmueble en garantía a cambio de una renta mensual durante un plazo pactado.

El proyecto surge de una entrevista con un experto en el tema (grabada en audio como evidencia académica, (`EntrevistaJuanDavid.mp3`), de la cual se extrajeron las variables de entrada, las variables de salida, la fórmula financiera y las reglas de negocio que rigen el cálculo.

## Descripción del problema

En una hipoteca inversa, el banco no le presta dinero a la persona para que ella pague cuotas, sino todo lo contrario: el banco le entrega una cuota mensual al propietario a cambio de quedarse con el derecho de cobro sobre el inmueble. El banco no hipoteca el 100% del valor del inmueble, sino solo un porcentaje de desembolso, para garantizar que pueda recuperar el capital entregado más los intereses causados durante todo el plazo.

## Variables de entrada

| Variable | Descripción | Restricción |
|---|---|---|
| Valor del inmueble | Valor comercial del inmueble | Debe ser mayor a 0 |
| % de desembolso | Porcentaje del valor del inmueble que el banco reconoce como base para hipotecar | Entre 0% y 100% |
| Tasa de interés mensual | Tasa pactada para el cálculo de la cuota | No puede superar el 4% mensual (tope de referencia del ejercicio) |
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
2. La tasa de interés mensual no puede superar el 4% mensual (tope de referencia del ejercicio).
3. El plazo en meses debe estar entre 1 y 240; valores en cero, negativos o mayores al límite se rechazan.

> **Nota:** la tasa máxima (4%) y el plazo máximo (240 meses) son supuestos de trabajo definidos para este ejercicio académico, no cifras oficiales confirmadas por una entidad reguladora. Sirven como valores de referencia razonables para las pruebas, y quedan sujetos a lo que confirme la entrevista con el experto.

## Casos de prueba

El proyecto incluye 10 casos de prueba construidos a partir de la entrevista con el experto: 3 normales, 3 extraordinarios y 4 de error. Están documentados en el libro de Excel `casos_de_prueba.xlsx` y automatizados como pruebas unitarias en `Tests_Hipoteca_Inversa.py`.

| # | Caso | Plazo | Detalle |
|---|------|-------|---------|
| 1-3 | Normales | 48-120 meses | Combinaciones válidas dentro de rangos normales |
| 4 | Extraordinario (tasa cero) | 36 meses | Promoción sin interés |
| 5 | Extraordinario (única disposición) | 1 mes | Pago único |
| 6 | Extraordinario (plazo máximo) | 240 meses | Límite superior del rango permitido |
| 7-10 | Error | — | Valor en cero, tasa que supera el 4%, plazo en cero, plazo negativo |

## Requisitos

- Python 3.10 o superior (el proyecto usa `unittest`, incluido en la librería estándar; no requiere instalar dependencias externas)

## Instalación

```bash
git clone https://github.com/Jose-Dv/Hipoteca-inversa
cd Hipoteca-inversa
```

## Uso

```bash
python main.py
```

El programa solicita el valor del inmueble, el porcentaje de desembolso, la tasa de interés mensual y el plazo en meses, y devuelve el valor efectivo, la cuota mensual, el total de abonos y el total de intereses, o el mensaje de error correspondiente si algún dato viola una regla de negocio.

## Pruebas

```bash
python -m unittest Tests_Hipoteca_Inversa -v
```

Los 10 casos de prueba (3 normales, 3 extraordinarios, 4 de error) están automatizados con `unittest` y todos pasan exitosamente sobre la lógica implementada en `Logica_Hipoteca_Inversa.py`.


## Metodología

1. Se realizó una entrevista grabada (audio) con un experto en hipoteca inversa para identificar variables de entrada, variables de salida y la fórmula de cálculo.
2. Con esa información se construyó el libro de Excel con los 10 casos de prueba (3 normales, 3 extraordinarios, 4 de error).
3. Se implementó la lógica de negocio en Python siguiendo la fórmula y las reglas de validación definidas para el ejercicio.
4. Se automatizaron los 10 casos de prueba como tests unitarios con `unittest` para verificar que el aplicativo cumple lo esperado.

## Autores

Sebastian Velasquez y
Jose Diaz
