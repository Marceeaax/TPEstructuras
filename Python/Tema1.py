import numpy as np
import seaborn as sns
import time
import csv
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


def traduccion(lenguaje):
# Se asume que Object Pascal es una extension de Pascal y uno de sus dialectos es Delphi
# Esta funcion nos ayuda a traducir un lenguaje con su enlace correspondiente en Github Topics
# Ejemplo: no existe la pagina https://github.com/topics/c++
# Si existe la pagina https://github.com/topics/cpp
# Esta traduccion puede o no ser necesaria para ingresar al link

    sinonimo = lenguaje
    
    sinonimos = {
    'C++': 'cpp',
    'C#': 'csharp',
    'Visual Basic': 'visual-basic',
    'Assembly language': 'assembly',
    'Delphi/Object Pascal': 'delphi',
    'Classic Visual Basic': 'visual-basic-6',
    '(Visual) FoxPro': 'vfp',
    'PL/SQL': 'plsql',
    }

    if lenguaje in sinonimos:
        sinonimo = sinonimos.get(lenguaje)
    
    return sinonimo

def insercion(arr1,arr2,arr3):
 
    # Ordenamiento por insercion, que suele ser eficaz con vectores no muy grandes
    # Extraido de geeksforgeeks
    for i in range(1, len(arr1)):
 
        key1 = arr1[i]
        if(len(arr2) > 0): key2 = arr2[i]
        if(len(arr3) > 0): key3 = arr3[i]

        j = i-1
        while j >= 0 and key1 > arr1[j] :
                arr1[j + 1] = arr1[j]
                if(len(arr2) > 0): arr2[j + 1] = arr2[j]
                if(len(arr3) > 0): arr3[j + 1] = arr3[j]
                j -= 1
        arr1[j + 1] = key1
        if(len(arr2) > 0): arr2[j + 1] = key2
        if(len(arr3) > 0): arr3[j + 1] = key3

# Link de las paginas a utilizar

URL1 = "https://www.tiobe.com/tiobe-index/"
URL2 = "https://github.com/topics/"

tiobe = requests.get(URL1)

soup = BeautifulSoup(tiobe.content, 'html5lib')

# buscamos todos los bloques que tengan el tag td
tdtags = soup.findAll('td')

# nos deshacemos de los tags td con una lista comprensiva
contenidotdtags = [td.get_text() for td in tdtags]

# declaramos la lista de lenguajes y lista de numero de repositorios como listas vacias
lenguajes = []
repositorios = []

# Debemos eliminar todos los elementos innecesarios de nuestra lista,
# Los lenguajes por posicion estan ubicados en los indices, 4, 11, 18....
# Esto supone un valor inicial de 4
# Un incremento de 7 por cada iteracion
# Como se requieren los 20 lenguajes mas populares, recorreremos hasta el indice 20*7 + 4 = 144

for i in range(4, 144, 7):
    lenguajes.append(contenidotdtags[i])

# variables requeridas para aplicar la ecuacion del rating de GitHub
max_numeroapariciones = 0
min_numeroapariciones = 0

# para cada uno de los 20 lenguajes
for i in range(len(lenguajes)):
    print("procesando " + lenguajes[i])
    # hacemos el http request y traduccion necesaria por si la necesite
    github = requests.get(URL2 + traduccion(lenguajes[i]))

    # esta parte hace que se repita el HTTP Request si recibimos algun error
    # el error mas comun es 429 (too many requests)
    while(github.status_code >= 400):
        print("Se produjo el error: ", github.status_code)
        print("Se deben esperar: ", github.headers['Retry-After'])
        print("Durmiendo por 10 segundos")
        time.sleep(10)
        github = requests.get(URL2 + traduccion(lenguajes[i]))

    print(github)
    print(URL2 + traduccion(lenguajes[i]))
    soup = BeautifulSoup(github.content, 'html5lib')
    # El numero de repositorios esta en un tag h2
    bloqueh2 = [h2.get_text() for h2 in soup.findAll("h2")]
    # Con expresiones regulares obtenemos los numeros de la cadena obtenida 

    #tuve bug con matlab aqui abajo, tarea averiguar
    numeros = re.findall('[0-9]+',bloqueh2[0])
    # Debido a que GitHub representa los numeros usando comas (ej: 123,456), la funcion anterior nos
    # arroja una lista con dos elementos de tipo cadena: 123 y 456, esto debe ser concatenado
    # y convertido a entero
    numerorepositorios = int(''.join([str(item) for item in numeros]))
    # Finalmente, agregamos el numero de repositorios a la lista
    repositorios.append(numerorepositorios)
    print("tiene " + str(numerorepositorios))

    if(numerorepositorios > max_numeroapariciones):
        max_numeroapariciones = numerorepositorios
    
    if(i == 0):
        min_numeroapariciones = numerorepositorios
    else:
        if(numerorepositorios < min_numeroapariciones):
            min_numeroapariciones = numerorepositorios

# dato interesante: Podemos crear un diccionario utilizando
# lenguajes_apariciones = {lenguajes[i]: repositorios[i] for i in range(len(lenguajes))}

# aqui guardamos los datos en un archivo csv
titulos = ['NOMBRE_LENGUAJE','NUMERO_APARICIONES']
formato = [lenguajes, repositorios]
# usamos la matriz transpuesta para dejar los datos de una manera mas prolija
filas = [[formato[j][i] for j in range(len(formato))] for i in range(len(formato[0]))]

with open('Resultados.csv','w', newline = '') as f: 
    write = csv.writer(f) 
    write.writerow(titulos) 
    write.writerows(filas) 

# calcular github rating
ratings = []

for i in range(len(repositorios)):
    rating = (repositorios[i]-min_numeroapariciones)/(max_numeroapariciones - min_numeroapariciones) * 100
    ratings.append(rating)

# Ordenar descendentemente por rating github
insercion(ratings,lenguajes,repositorios)

# Imprimir resultados
print("NOMBRE_LENGUAJE" + "       " + "RATING_GITHUB" + "         " + "NRO_APARICIONES")
for i in range(len(lenguajes)):
    print(lenguajes[i], end ='')
    if(len(lenguajes[i]) < 22):
        for j in range(22 - len(lenguajes[i])):
            print(" ",end ='')
    print(ratings[i],end ='')
    if(len(str(ratings[i])) < 22):
        for k in range(22 - len(str(ratings[i]))):
            print(" ",end ='')
    print(repositorios[i])


# Aqui comienza el grafico de barras

insercion(repositorios,lenguajes,[])

lenguajesgrafico = lenguajes[:10]
repositoriosgrafico = repositorios[:10]

listaTopicsDF = {'NOMBRE_LENGUAJE': lenguajesgrafico, 'NRO_APARICIONES': repositoriosgrafico}

df=pd.DataFrame(listaTopicsDF)

fig,ax = plt.subplots(figsize=(20,6))

fig.patch.set_facecolor('black')

sns.cubehelix_palette(start=2, rot=0, dark=0, light=.95, reverse=True, as_cmap=True)

csfont = {'fontname':'Source Code Pro'}

sns.barplot(x='NOMBRE_LENGUAJE',y='NRO_APARICIONES',data=df,ci=95,palette="crest",ax=ax,color='white')

ax.set_title("TEMA 1\nNumero de repositorios por lenguaje",**csfont,color='white')

ax.tick_params(axis='y',labelsize=16,length=0,colors='gray')
ax.tick_params(axis='x',labelsize=8,length=0,pad=2,colors='grey')

# method 1
ax.spines['left'].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
#method 2
plt.box(False)

# add grid lines for y axis
ax.yaxis.grid(linewidth=0.5,color='gray')
# put the grid lines below bars
ax.set_axisbelow(True)

ax.set_xlabel('NOMBRE_LENGUAJE',labelpad=-5,weight='bold',size=10,**csfont,c='grey')
ax.set_ylabel('NRO_APARICIONES',labelpad=15,weight='bold',size=15,**csfont,c='grey')

plt.xticks(rotation=30,color='#565656')

plt.show()
