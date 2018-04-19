
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
L = []

for line in reader:

       przewidywana_klasa.append(int(line[0]))
       prawdopodobienstwa_lista.append(line[1:])
       L.append(line)



# Rysowanie
#print(przewidywana_klasa) 
#print(prawdopodobienstwa_lista)


TP = [0]*n_klas # Liczba przewidywanych i rzeczywistych bedacych prawda
FP = [0]*n_klas # Liczba przewidywanych prawdziwych oraz rzeczywistych falszywych
TN = [0]*n_klas
FN = [0]*n_klas

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
for i in range (0,n_klas):
    for el in range(0,len(przewidywana_klasa)):
         pk_el = przewidywana_klasa[el]
         if RV[i] == pk_el:
           TP[pk_el] = TP[pk_el] + 1
         if (i == pk_el) and (RV[el]!=pk_el):
            FP[i]=FP[i]+1
         if (i!=pk_el) and (RV[el]==pk_el):
            FN[i]=FN[i]+1


#Wyliczamy TN dla klasy i oraz ilosc wszystkich pozytywnych i negatywnych szacowan
for i in range (0,n_klas):
    TN[i] = len(przewidywana_klasa) - TP[i] - FN[i] - FP[i]
    N[i] = FN[i] + TN[i]
    P[i] = TP[i] + FP[i]


ROC = []
#lista punktow wykresu

Li = L

for i in range (0,n_klas):

    Li = (sorted(L,key=lambda x: x[i+1],reverse=True))
    fp = 0
    tp = 0
    n = N[i]
    p = P[i]

    j = 1
    print("------------------------------------------------------------")
    while j < len(L):

        maxi = max(Li[j][1:])

        maxi_index = (Li[j].index(maxi))-1

        if(L[j-1][maxi_index] != Li[j][maxi_index]):

            ROC.append([i,fp/n,tp/p])
            Li[j-1][maxi_index] = Li[j][maxi_index]

        if(float(Li[j][0]) == float(maxi_index)):
           tp = tp+1

        else:
            fp = fp+1

        j = j +1

file = open('testfile.txt','w') 

for el in range(len(ROC)):
       print(ROC[el])

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
