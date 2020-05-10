
import random

pesos = [random.uniform(0,1), random.uniform(0,1)]
llindar = 0.5
aprenent = True
bucles = 0
acerts = 0

taula = [[1,1,1], [1,0,0],[0,1,0],[0,0,0]]

while aprenent == True:
    for x in taula:
        if (x[0]*pesos[0]+x[1]*pesos[1]) > llindar:
            sortida_polaritzada = 1
            bucles += 1
        else:
            sortida_polaritzada = 0
            bucles += 1
            
        if sortida_polaritzada == x[2]:
            acerts += 1
        else:
            error = x[2] - sortida_polaritzada
            pesos[0] += (0.1 * error * x[0]) 
            pesos[1] += (0.1 * error * x[1])
            acerts = 0
            
        if acerts == 4:
            print(pesos)
            print(bucles -4)
            aprenent= False

            
