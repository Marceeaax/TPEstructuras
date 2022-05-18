library("rvest")
library("dplyr")
library("lubridate")
library("hash")
library("scriptName")

insercion <- function(x,x1,x2)
{
	n <- length(x)
	for (i in 2 : n)
	{
		key = x[i]
		if(!missing(x1)) key1 = x1[i]
		if(!missing(x2)) key2 = x2[i]
		j   = i - 1
		while (j > 0 && key > x[j])
		{
			x[j + 1] = x[j]
			if(!missing(x1)) x1[j + 1] = x1[j]
			if(!missing(x2)) x2[j + 1] = x2[j]
			j = j - 1
		}
		x[j + 1] = key
		if(!missing(x1)) x1[j + 1] = key1
		if(!missing(x2)) x2[j + 1] = key2
	}
	return(list(x,if(!missing(x1)) x1,if(!missing(x2)) x2))
}

topicos <- hash()
topicosdf <- data.frame()
#cantidad de tiempo para 30 dias
horas30dias<- ymd_hms("2022-01-31 00:00:00") - ymd_hms("2022-01-01 00:00:00")

#iterar todas las paginas
for (page_result in seq(from = 1, to = 2, by = 1)) {
  
  link<-paste0("https://github.com/topics/angular?page=",page_result)
  page<- read_html(link)
  #trae los topics sin tener en cuenta las fechas
  #topic<- page %>% html_nodes(".f6.mb-2") %>% html_text()
  
  conjuntoTopicPorFecha<- page %>% html_nodes("#js-pjax-container .pb-2") 
  
  update<- page %>% html_nodes(".mr-4 .no-wrap") %>% html_attr("datetime")  
  
  #iterando sobre las etiquetas articulos, se seleccionan los topics que estan en el rango
  for(indice in seq(from=1,to=length(update),by=1)){
    print(paste("indice:",indice))
    difEntreDias<- as_datetime(Sys.Date()) - as_datetime(update[indice]) 
    print(paste("diferenciaEntreDias:",difEntreDias,"update:",update[indice],"Es menor?",difEntreDias<=horas30dias))
    if(difEntreDias<=horas30dias){
      #print(paste(difEntreDias<=horas30dias))
      topic<-conjuntoTopicPorFecha[[indice]] %>% html_text()
      #print(paste("Topic:",topic))
      separar<- gsub("\\s+"," ",topic)
      separar<-substring(separar,2,nchar(separar))
      #print(paste("Separar:",separar))
      topicsPorFecha <- strsplit(separar," ")
      #print(paste("TopicsPorFecha:",topicsPorFecha))
      
      for(i in 1:length(unlist(topicsPorFecha))){
            if(has.key(unlist(topicsPorFecha)[i],topicos)){
                topicos[unlist(topicsPorFecha)[i]] = topicos[[unlist(topicsPorFecha)[i]]] + 1
            }
            else{
                .set(topicos,unlist(topicsPorFecha)[i],1)
            }
      }
      #topicos2 <- rbind(topicos2, topicsPorFecha)



      #print(paste("Topicos dataFrame:",topicos))
    }
  }
}

df <- data.frame(TOPIC = keys(topicos),
                 NUMERO_APARICIONES = values(topicos)
                 )

#ubicacion de nuestro script
ubicacion <- strsplit(current_filename(), "")[[1]]

for(i in length(ubicacion):1){
    if(ubicacion[i] == "\\"){
        break
    }
}
punto = i

ubicacion = substring(current_filename(),1,i)
ubicacion = gsub("\\\\","/",ubicacion)

write.csv(df,paste0(ubicacion,"ResultadosTema2.csv"), row.names = FALSE)

listaordenada = insercion(values(topicos),keys(topicos))

#par(mar=c(3, 15, 3, 10))

jpeg('Tema2grafico.jpg')

barplot(rev(head(unlist(listaordenada[1]),20)),names.arg=rev(head(unlist(listaordenada[2]),20)),beside = FALSE, horiz = TRUE, angle = 45,col="darkblue",density=100, main="20 palabras con mayor numero de apariciones",border="black",las=1)

ubicacion = gsub("/","\\",ubicacion)

print(paste0("Se ha guardado un PDF con la grafica y un CSV con los resultados en: ",substring(current_filename(),1,punto-1)))

dev.off()

topicos

