import requests
import time
import csv
from datetime import datetime
import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

listaTopics = dict()

reposexaminados = 0

URL = "https://github.com/topics/lua?o=desc&s=updated"

topicinteres = requests.get(URL)

#aqui obtenemos la hora utc que utiliza github
tiempoutcauxiliar = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d%H:%M:%S")
tiempoutc = datetime.datetime.strptime(tiempoutcauxiliar, "%Y-%m-%d%H:%M:%S")

soup = BeautifulSoup(topicinteres.content, 'html5lib')

# extraer todos los div que tienen los topicos
div = soup.findAll("div",{"class":"color-bg-default rounded-bottom-2"})

#extraer la linea que tiene el tiempo
tiempo = div[0].find("relative-time")

#extraer la cadena de la fecha con la hora
tiempocadena = tiempo.get("datetime")

# ordenamiento de datos
tiempocadena = tiempocadena.replace('T','')
tiempocadena = tiempocadena.replace('Z','')

objetotiempo = datetime.datetime.strptime(tiempocadena, "%Y-%m-%d%H:%M:%S")

tiempoTranscurrido = tiempoutc - objetotiempo


for i in range(len(div)):

    #
    litags = div[i].parent.findAll("li")

    if(litags[1].find("a").get("aria-current") != 'true'):

        reposexaminados += 1

        #extraer la linea que tiene el tiempo
        tiempo = div[i].find("relative-time")
        #extraer la cadena de la fecha con la hora
        tiempocadena = tiempo.get("datetime")

        # ordenamiento de datos
        tiempocadena = tiempocadena.replace('T','')
        tiempocadena = tiempocadena.replace('Z','')

        objetotiempo = datetime.datetime.strptime(tiempocadena, "%Y-%m-%d%H:%M:%S")

        tiempoTranscurrido = tiempoutc - objetotiempo

        if(tiempoTranscurrido.days <= 30):
            tagsA = div[i].findAll("a")

            for j in range(len(tagsA)):
                tagA = tagsA[j]

                # a veces encontramos un link en la descripcion del repo, y eso puede entrar como topic
                # por tener tambien un tag <a>
                # para deshacernos de ese caso particular, utilizamos este if
                if(tagA.get("class") != None):
                    topicAsociadoaux = tagA.string
                    topicAsociado = topicAsociadoaux.replace(' ','')
                    topicAsociado = topicAsociado.replace('\n','')
                    print(topicAsociado)

                    if topicAsociado in listaTopics.keys():
                        listaTopics[topicAsociado] += 1
                    else:
                        listaTopics[topicAsociado] = 1

# Esta ordenacion solo es posible en python 3.7+ o CPython 3.6
listaTopics = {k: v for k, v in sorted(listaTopics.items(), key=lambda item: item[1], reverse= True)}

for j in listaTopics:
	print("La palabra",j,"aparece",listaTopics[j],"",end='', flush=True)
	print("vez") if listaTopics[j] == 1 else print("veces")

print("Numero de repos examinados: ", reposexaminados)

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

fig = plt.figure(figsize = (100, 50))

plt.bar(topicsgrafico, aparicionesgrafico, color ='maroon',
        width = 0.4)

plt.xlabel("Topics")
plt.ylabel("Numero de apariciones")
plt.title("Numero de apariciones de cada topic")
plt.show()




