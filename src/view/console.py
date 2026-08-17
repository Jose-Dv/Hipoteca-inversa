#Consola de el proyecto de hipoteca inversa
from src.model import logica_hipoteca_inversa

print("Este programa permite calcular la hipoteca inversa, en base a: \n 1.Valor Propiedad \n 2.Porcentaje de desembolso \n 3.Tasa de interes \n 4.Plazo en meses ")

valor = float(input("Valor Propiedad: "))
desembolso = float(input("Porcentaje de desembolso: ")) / 100
tasa = float(input("Tasa de interes: ")) / 100
plazo = int(input("Plazo en meses: "))

try:
    cuota, abonos, intereses = logica_hipoteca_inversa.desembolso_mensual(valor, desembolso, tasa, plazo)
    print("Cuota mensual:", cuota)
    print("Total abonos:", abonos)
    print("Total intereses:", intereses)
except logica_hipoteca_inversa.ValorPropiedad0 as error:
    print(error)
except logica_hipoteca_inversa.HipotecaUsura as error:
    print(error)
except logica_hipoteca_inversa.PlazoMayor240 as error:
    print(error)
except logica_hipoteca_inversa.PlazoMenorIgual0 as error:
    print(error)
