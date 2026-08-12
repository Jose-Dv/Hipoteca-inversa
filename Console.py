#Consola de el proyecto de hipoteca inversa

import Logica_Hipoteca_Inversa

print("Este programa permite calcular la hipoteca inversa, en base a: \n 1.Valor Propiedad \n 2.Porcentaje de desembolso \n 3.Tasa de interes \n 4.Plazo en meses ")

valor = float(input("Valor Propiedad: "))
desembolso = float(input("Porcentaje de desembolso: ")) / 100
tasa = float(input("Tasa de interes: ")) / 100
plazo = int(input("Plazo en meses: "))

try:
    cuota, abonos, intereses = Logica_Hipoteca_Inversa.desembolso_mensual(valor, desembolso, tasa, plazo)
    print("Cuota mensual:", cuota)
    print("Total abonos:", abonos)
    print("Total intereses:", intereses)
except Logica_Hipoteca_Inversa.ValorPropiedad0 as error:
    print(error)
except Logica_Hipoteca_Inversa.HipotecaUsura as error:
    print(error)
except Logica_Hipoteca_Inversa.PlazoMayor240 as error:
    print(error)
except Logica_Hipoteca_Inversa.PlazoMenorIgual0 as error:
    print(error)
