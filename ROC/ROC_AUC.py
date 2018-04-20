
import csv
import sys

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

# Import danych
file = open('input_popr.csv')
reader = csv.reader(file)
n_klas = int(file.readline())
L = []

for line in reader:

       L.append(line)

#Tworzenie pustych list odpowiednio dla wartosci ROC czulosci 
ROC = []
czulosci =[]*n_klas # oznacza ze utworzy n_klas-elementowa pusta liste
swoistosci = []*n_klas
swoistosc_klasy = []
czulosc_klasy = []

Li = L #kopiuje liste by dzialac na kopii a w pamieci miec oryginal

for i in range (0,n_klas):

    Li = (sorted(L,key=lambda x: x[i+1],reverse=True))#sort malejacy po i+1 rzedzie listy L (klasa,praw0,praw1,praw2....)
    n = len(Li) #pobieram rozmiar Li - ilosc obserwacji
    Lista_przewidywanych = [1]*n # poczatkowo dla kazdej klasy przewiduje ze bedzie 1 czyli  prawda
    Lista_rzeczywistych_rekod = [0]*n # pusta lista n elementow - do zapelnienia
    Lista_prawdopodobienstw_dla_klasy_i = [0]*n 

    for j in range (0,n):

        Lista_prawdopodobienstw_dla_klasy_i[j] = Li[j][i+1]  #posortowane prawdopodobienstwa dla klasy i

        if(float(Li[j][0]) == float(i)):
          Lista_rzeczywistych_rekod[j] = 1 #pobieramy pierwsza kolumne z posortowanej tabeli i jezeli jej wartosc = nr klasy - kodujemy jako 1 -[rawda

        else:
            Lista_rzeczywistych_rekod[j] = 0#kodujemy jako falsz

    prog = 0  #element do ktorego porownujemy prawdopodobienstwa
    czulosc = 0 #poczatkowa wartosc czulosci
    swoistosc = 0
    j = 1

    print("--------------------------OBLICZANIE PUNKTOW KRZYWEJ ROC DLA KLASY "+str(i)+"--------------------------")

    while j < len(Li)-1:

        fp = 0 #dla kazdego przejscia po liscie zerujemy fp tp fn i tn
        tp = 0
        fn = 0
        tn = 0

        #przechodzimy po obserwacjach i sprawdzamy ...

        for k in range (0,n):

             if(float(Lista_przewidywanych[(n-1) - k]) == 0 and float(Lista_rzeczywistych_rekod[(n-1) - k]) == 0):
                   tn = tn + 1
             if(float(Lista_przewidywanych[(n-1) - k]) == 0 and float(Lista_rzeczywistych_rekod[(n-1) - k]) == 1):
                  fn = fn + 1
             if(float(Lista_przewidywanych[(n-1) - k]) == 1 and float(Lista_rzeczywistych_rekod[(n-1) - k]) == 0):
                   fp = fp + 1
             if(float(Lista_przewidywanych[(n-1) - k]) == 1 and float(Lista_rzeczywistych_rekod[(n-1) - k]) == 1):
                   tp = tp + 1

    #Liczenie czulosci i swoistosci, dodanie do listy pktow ROC
        if((tp + fn) > 0):
                  czulosc = float(tp / (tp + fn))
        if((tn + fp) > 0):
               swoistosc = float(tn / (tn +fp))

        if([i,round(float(1-swoistosc),3),round(czulosc,3)] not in ROC):
               ROC.append([i,round(float(1-swoistosc),3),round(czulosc,3)])

    #porownywanie prawdopodobienstw do progu i modyfikacja
        for l in range (0,n):
         if(float(prog) >= float(Lista_prawdopodobienstw_dla_klasy_i[l])):
               Lista_przewidywanych[l] = 0
         else:
                Lista_przewidywanych[l] = 1

        prog = Lista_prawdopodobienstw_dla_klasy_i[len(Lista_prawdopodobienstw_dla_klasy_i)-j]
        j = j+ 1

#Wydzielamy z listy ROC - 2 listy czulosci i swoistosci
for j in range (0,n_klas):
    swoistosc_klasy=[]
    czulosc_klasy=[]
    for i in range (0,len(ROC)):

        if (ROC[i][0] == j):
            swoistosc_klasy.append(ROC[i][1])
            czulosc_klasy.append(ROC[i][2])

    czulosci.append(czulosc_klasy)
    swoistosci.append(swoistosc_klasy)

AUC = [0]*n_klas

#Wyliczanie AUC - metoda prostokatow
for i in range (0,len(swoistosci)):
       for j in range (1,len(czulosci[i])):
           AUC[i] = AUC[i] + czulosci[i][j-1]*(swoistosci[i][j] - swoistosci[i][j-1])

#RYSSOWANIE WYKRESU
legenda = []
print(legenda)

plt.figure()
legend_lines = []

colors = ['crimson', 'blue', 'green','darkorange','chocolote','magenta','cyan','pink','violet','maroon']

for i in range (0,n_klas):
    plt.plot(swoistosci[i],czulosci[i], color = colors[i], linewidth=2)
    legenda.append("Wykres dla klasy " + str(i) + ", AUC ="+ str(round(AUC[i],3)))
    legend_lines.append(plt.plot([1,2,3], label= legenda[i],color = colors[i]))

plt.legend(legend_lines)
plt.plot([0, 1], [0, 1], '-', lw=4,color = "black")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('100 - Czułość')
plt.ylabel('Czułość')
plt.title('Wykres ROC dla k-klas')
plt.legend(loc="lower right")
plt.show()

