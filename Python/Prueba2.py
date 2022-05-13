import requests
import time
import csv
from datetime import datetime
import datetime
from bs4 import BeautifulSoup
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Puede elegir un numero entre 1 a 34 paginas para examinar, la pagina 35 no existe para ningun topic
cargarPaginas = 34
soups = []
listaTopics = dict()
reposexaminados = 0
reposactualizados = 0

URL = "https://github.com/topics/java?o=desc&s=updated&page="

for i in range(cargarPaginas):
    print("Enviando HTTPRequest a la pagina " + str(i+1) + " del topic Java")
    pagina = requests.get("https://github.com/topics/java?o=desc&s=updated&page=" + str(i))
    while(pagina.status_code >= 400):
        print("Se produjo el error: ", pagina.status_code)
        print("Se deben esperar: ", pagina.headers['Retry-After'])
        print("Durmiendo por 70 segundos")
        time.sleep(70)
        pagina = requests.get("https://github.com/topics/java?o=desc&s=updated&page=" + str(i))
    soups.append(BeautifulSoup(pagina.content,'html5lib'))

print("Longitud de soups es " + str(len(soups)))
tiempoutcauxiliar = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d%H:%M:%S")
tiempoutc = datetime.datetime.strptime(tiempoutcauxiliar, "%Y-%m-%d%H:%M:%S")

# por cada pagina
for i in range(cargarPaginas):
    print("-------PAGINA " + str(i+1) + " ---------")
    # extraer todos los div que tienen los topicos
    div = soups[i].findAll("div",{"class":"color-bg-default rounded-bottom-2"})
        
    #extraer la linea que tiene el tiempo
    tiempo = div[0].find("relative-time")

    #extraer la cadena de la fecha con la hora
    tiempocadena = tiempo.get("datetime")

    # ordenamiento de datos
    tiempocadena = tiempocadena.replace('T','')
    tiempocadena = tiempocadena.replace('Z','')

    objetotiempo = datetime.datetime.strptime(tiempocadena, "%Y-%m-%d%H:%M:%S")

    tiempoTranscurrido = tiempoutc - objetotiempo


    for j in range(len(div)):
        print("-------REPOSITORIO " + str(j+1) + " ---------")
        litags = div[j].parent.findAll("li")

        if(litags[1].find("a").get("aria-current") != 'true'):
            reposexaminados += 1

            #extraer la linea que tiene el tiempo
            tiempo = div[j].find("relative-time")
            #extraer la cadena de la fecha con la hora
            tiempocadena = tiempo.get("datetime")

            # ordenamiento de datos
            tiempocadena = tiempocadena.replace('T','')
            tiempocadena = tiempocadena.replace('Z','')

            objetotiempo = datetime.datetime.strptime(tiempocadena, "%Y-%m-%d%H:%M:%S")

            tiempoTranscurrido = tiempoutc - objetotiempo

            if(tiempoTranscurrido.days <= 30):
                reposactualizados += 1
                tagsA = div[j].findAll("a")

                for k in range(len(tagsA)):
                    tagA = tagsA[k]

                    # a veces encontramos un link en la descripcion del repo, y eso puede entrar como topic
                    # por tener tambien un tag <a>
                    # para deshacernos de ese caso particular, utilizamos este if
                    if(tagA.get("class") != None):
                        topicAsociadoaux = tagA.string
                        topicAsociado = topicAsociadoaux.replace(' ','')
                        topicAsociado = topicAsociado.replace('\n','')
                        #print(topicAsociado)

                        if topicAsociado in listaTopics.keys():
                            listaTopics[topicAsociado] += 1
                        else:
                            listaTopics[topicAsociado] = 1

listaTopics = {k: v for k, v in sorted(listaTopics.items(), key=lambda item: item[1], reverse= True)}

for j in listaTopics:
	print("La palabra",j,"aparece",listaTopics[j],"",end='', flush=True)
	print("vez") if listaTopics[j] == 1 else print("veces")

print("Numero de repos examinados: ", reposexaminados)
print("Numero de repos que cumplen con la condicion: ", reposactualizados)

titulos = ['TOPIC','NRO_APARICIONES']
topics = list(listaTopics.keys())
apariciones = list(listaTopics.values())
formato = [topics,apariciones]
filas = [[formato[j][i] for j in range(len(formato))] for i in range(len(formato[0]))]

with open('ResultadosTema2.csv','w', newline = '') as f: 
    write = csv.writer(f) 
    write.writerow(titulos)
    write.writerows(filas)

# extraer los 20 primeros topics
topicsgrafico = topics[:20]
aparicionesgrafico = apariciones[:20]

print({'TOPIC': topicsgrafico, 'NRO_APARICIONES': aparicionesgrafico})

listaTopicsDF = {'TOPIC': topicsgrafico, 'NRO_APARICIONES': aparicionesgrafico}

df=pd.DataFrame(listaTopicsDF)

fig,ax = plt.subplots(figsize=(9,6))

sns.barplot(x='TOPIC',y='NRO_APARICIONES',data=df,ci=95,ax=ax)

ax.set_title("Topics asociados de los repositorios actualizados en los ultimos 30 dias")

ax.tick_params(labelsize=16,length=0)

# method 1
ax.spines['left'].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
#method 2
plt.box(False)

sns.color_palette("flare", as_cmap=True)

# add grid lines for y axis
ax.yaxis.grid(linewidth=0.5,color='black')
# put the grid lines below bars
ax.set_axisbelow(True)

ax.set_xlabel('TOPIC',weight='bold',size=15)
ax.set_ylabel('NRO_APARICIONES',weight='bold',size=15)

plt.xticks(rotation=30,color='#565656')

plt.show()


