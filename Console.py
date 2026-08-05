# consola de el proyecto de hipoteca inversa

import Logica_Hipoteca_Inversa
print("Este programa permite calcular la hipoteca inversa, en base a: \n 1.Valor Propiedad \n 2.Porcentaje de desembolso \n 3.Tasa de interes \n 4.Plazo en meses ")
valor = float(input("Valor Propiedad: "))
desembolso = float(input("Porcentaje de desembolso: "))
tasa = float(input("Tasa de interes: "))
plazo = int(input("Plazo en meses: "))

print(Logica_Hipoteca_Inversa.desembolso_mensual(valor,desembolso,tasa,plazo))
