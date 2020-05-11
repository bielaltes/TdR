'''
Implementació perceptró multicapa adaptatiu

@bielaltes
'''
import random, json, numpy


class MLP:
    def __init__(self):
        print("#### YOU'RE RUNNING BIEL'S PERCEPTRON ###")
        self.perceptro = []
        self.sortides = []
        self.training_data = []
        self.executing_data = []
        self.alpha = 0.11
        self.S_d = []
        self.mode = bool

        entrenar_executar = input("Vols entrenar (1) o executar (2) el perceptro mutlicapa?: ")
        if entrenar_executar == "1":
            self.mode = True
            with open('training_data.txt', 'r') as training:
                self.training_data = json.load(training)
            nova_creada = input("El MLP es nou (1) o ja l'havies entrenat abans (2)?: ")
            
            if nova_creada == "1":
                numero_capes = int(input("Selecciona el numero de capes: "))
                for x in range(numero_capes):
                    capa = []
                    z = []
                    w = []
                    b = []
                    neurones_per_capa = []
                    neurones_per_capa.append(int(input('numero de neurones a la capa ' + str(x) + ' : ')))
                    for y in range(int(neurones_per_capa[-1])):
                        b.append(random.random())
                        z.append(random.random())
                        w_per_capa = []
                        if x != 0:
                            for k in range(len(self.perceptro[x-1][0])):
                                w_per_capa.append(random.random())
                        w.append(w_per_capa)
                    capa.append(b)
                    capa.append(w)
                    self.perceptro.append(capa)
                    self.sortides.append(z)
                self.exeucio()
                self.guardar()
                
            elif nova_creada == "2":
                with open('estructura_perceptro.txt', 'r') as estructura_perceptro:
                    estructura_completa = json.load(estructura_perceptro)
                    self.perceptro = estructura_completa[0]
                    self.sortides = estructura_completa[1]
                self.exeucio()
                self.guardar()
                
            else:
                print("error")

        elif entrenar_executar == "2":
            self.mode = False
            with open('executing_data.txt', 'r') as executing:
                self.executing_data = json.load(executing)
            with open('estructura_perceptro.txt', 'r') as estructura_perceptro:
                estructura_completa = json.load(estructura_perceptro)
                self.perceptro = estructura_completa[0]
                self.sortides = estructura_completa[1]
            self.exeucio()

        else:
            print("error")
            

    def exeucio(self):
        nombre_bucles = 0
        
        if self.mode == True:
            for y in range(int(input("Quants cops vols entrenar el bucle?: "))):
                for x in range(int(len(self.training_data))):
                    self.sortides[0] = self.training_data[x][0]
                    self.sortida()
                    self.S_d = []
                    self.S_d = self.training_data[x][1]
                    self.retropropagacio()
                nombre_bucles += 1
                print("Portes "+ str(nombre_bucles) +" bucles")
                if nombre_bucles % 10 == 0:
                    self.guardar()
        else:
            acerts = 0
            errors = 0
            for x in range(int(len(self.executing_data))):
                self.sortides[0] = self.executing_data[x][0]
                self.sortida()
                for i in range(len(self.sortides[-1])):
                    if numpy.isclose(self.sortides[-1][i],self.executing_data[x][1][i], atol=0.1):
                        acerts += 1
                    else:
                        errors += 1
                        print("error")
            percentatge_acerts = ((acerts/(acerts+errors))* 100)
            print(percentatge_acerts)


    def sortida(self): #executa el perceptro i retorna la sortida
        
        for k in range(len(self.perceptro)-1):
            for i in range(len(self.sortides[k+1])):
                sortida_neurona = 0
                for j in range(len(self.sortides[k])):
                    sortida_neurona += (self.sortides[k][j] * self.perceptro[k+1][1][i][j])
                sortida_neurona += self.perceptro[k+1][0][i]
                if sortida_neurona > 15:
                    sortida_neurona = 1
                elif sortida_neurona < -15:
                    sortida_neurona = 0
                else:
                    sortida_neurona = (1/( 1 + numpy.exp(-sortida_neurona)))
                self.sortides[k+1][i] = sortida_neurona
                
        if self.mode == False:
            print(self.sortides[-1])


    def retropropagacio(self): #un cop obtinguda la sortida i comparada amb el que s'havia esperat,

        delta_y = []
        for k in range(len(self.sortides[-1])):
            delta_y.append(self.sortides[-1][k] * (1 - self.sortides[-1][k]) * (self.sortides[-1][k] - self.S_d[0]))

            for y in range(len(self.sortides[-2])):
                self.perceptro[len(self.perceptro)-1][1][k][y] -= self.alpha * self.sortides[-2][y] * delta_y[k]
            self.perceptro[len(self.perceptro)-1][0][k] -= self.alpha * delta_y[k]

        for p in range(len(self.sortides)-2):
            delta_t = []
            sumatori_retropropagacio = 0
            
            for k in range(len(self.sortides[-2-p])):
                for j in range(len(self.sortides[-3-p])):
                    for i in range(len(self.sortides[-1-p])):
                        sumatori_retropropagacio += delta_y[i] * self.perceptro[len(self.perceptro)-1 -p][1][i][k]
                delta_t.append((self.sortides[-2-p][k] * (1-self.sortides[-2-p][k])) * sumatori_retropropagacio)
                for n in range(len(self.sortides[-3-p])):
                    self.perceptro[len(self.perceptro)-2-p][1][k][n] -= self.alpha * self.sortides[-3-p][n] * delta_t[k]
                self.perceptro[len(self.perceptro)-2-p][0][k] -= self.alpha * delta_t[k]
            delta_y = delta_t
            pass


    def guardar(self):
        estructura_perceptro = [self.perceptro, self.sortides]
        with open('estructura_perceptro.txt', 'w') as perceptro:
            json.dump(estructura_perceptro, perceptro)
        print("Guardat correctament")
MLP()

