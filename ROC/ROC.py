#Do poprawnego działania programu wymagana jest instalacja oprogramowania - Anaconda 3.6.5 
#zawiera ona oprogramowanie do obliczen statystycznych dla języka Python
import csv 
import sys

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle



# Import danych
file = open('input_popr.csv')
reader = csv.reader(file)
n_klas = int(file.readline())

przewidywana_klasa = []
prawdopodobienstwa_lista = []

for line in reader:
      
       przewidywana_klasa.append(int(line[0]))
       prawdopodobienstwa_lista.append(line[1:])


# Rysowanie
#print(przewidywana_klasa) 
#print(prawdopodobienstwa_lista)


TP = [0]*n_klas # Liczba przewidywanych i rzeczywistych bedacych prawda
FP = [0]*n_klas # Liczba przewidywanych prawdziwych oraz rzeczywistych falszywych

N = [0]*n_klas #Liczba blednych oszacowan
P = [0]*n_klas #liczba poprawnych oszacowan



RV = [] #lista z wartosciami zawierajaca numery klas, ktorych prawdopodobienstwa sa najwiszeksze
#Wyszukujemy klase z najwiekszym prawdopodobienstwem
for el in prawdopodobienstwa_lista:
    m = max(el)    
    for j in range(0,n_klas):
            if(el[j] == m):
                    RV.append(j)
n =0

#porownanie wartosci RV z przewidywanymi klasami - przewidywana_klasa
#wyliczenie ilosci poprawnych i niepoprawnych szacowan

for el in range(0,len(przewidywana_klasa)):
    pk_el = przewidywana_klasa[el]
    if RV[el] == pk_el:
        P[pk_el] = P[pk_el] + 1
    else:
           N[pk_el] = N[pk_el] + 1

P_wszystkie = sum(P)
N_wszystkie = sum(N)


for i in range(0,n_klas):
    TP[i] = P[i]
    FP[i] = N[i]


print(TP)
print(FP)

plt.figure()
line_width = 2

colors = cycle(['gold', 'red', 'teal','darkorange','chocolote','magenta','cyan','pink','green','maroon'])
#for i, color in zip(range(n_classes), colors):
   ##         label='AUC dla klasy {0} (AUC = {1:0.2f})'
      #       ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=1)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('100 - Czułość')
plt.ylabel('Czułość')
plt.title('Wykres ROC dla k-klas')
plt.legend(loc="lower right")
plt.show()
