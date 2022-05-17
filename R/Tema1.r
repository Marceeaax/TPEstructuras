# Se deben instalar primeramente
# install.packages("rvest")
# install.packages("scriptName")

library(rvest)
library(scriptName)

traductor <- function(palabra){
	lenguajesproblematicos <- c("C++","C#","Visual Basic","Assembly language","Delphi/Object Pascal","Classic Visual Basic","(Visual) FoxPro","PL/SQL")
	
	sinonimos <- c("cpp","csharp","visual-basic","assembly","delphi","visual-basic-6","vfp","plsql")

	if(!(is.na(match(palabra,lenguajesproblematicos)))){
		return(toString(sinonimos[match(palabra,lenguajesproblematicos)]))
	}
	
	return(palabra)
}

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

tiobe_url <- read_html("https://www.tiobe.com/tiobe-index/")
#Leemos el ranking TIOBE

td_tags <- html_nodes(tiobe_url, "td") %>% html_text()
#Obtenemos todos los tags td

td_tags = head(td_tags, 138)
#extraemos todos los elementos hasta la posicion138
#El tag en la posicion 138 contiene el puesto 20 en el ranking TIOBE

lenguajes = list()
repositorios = list()
ratings = list()
#creamos una lista

for(i in 1:length(td_tags)){
	if((i-5)%%7 == 0){   
	lenguajes <- append(lenguajes,td_tags[i])
	}
}

for(i in 1:length(lenguajes)){
	numero = ""
	print(paste0("procesando ",lenguajes[i]))
	
	github = list()

	while (length(github) == 0){
	tryCatch(               
	# Specifying expression
	expr = {                     
		github <- read_html(paste0("https://github.com/topics/",traductor(toString(lenguajes[i]))))
		print("Pagina procesada con exito.")
	},
	# Specifying error message
	
	warning = function(w){      
		
	},
	error = function(e){         
		print("Hubo un error al procesar la pagina. El sistema esperara unos cuantos segundos")
		Sys.sleep(7)
		close(github)
		closeAllConnections()
		#gc()
		}
	)
	}

	textorepo <- html_nodes(github, ".h3") %>% html_text()

	numberstring_split <- strsplit(textorepo, "")[[1]]

	for (i in 1:length(numberstring_split)) {
  	if(length(grep("[0-9]+",numberstring_split[i])) > 0){
		numero <- paste0(numero,numberstring_split[i])
	}
	}
	
	repositorios <- append(repositorios,strtoi(numero))
}

df <- data.frame(NOMBRE_LENGUAJE = unlist(lenguajes),
                 NUMERO_APARICIONES = unlist(repositorios)
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

write.csv(df,paste0(ubicacion,"Resultados.csv"), row.names = FALSE)

# calculo del rating

for(i in 1:length(lenguajes)){
	rating = (as.numeric(repositorios[i])-min(unlist(repositorios)))/(max(unlist(repositorios)) - min(unlist(repositorios))) * 100
	ratings <- append(ratings,rating)
}

listapantalla <-insercion(unlist(ratings),unlist(repositorios),unlist(lenguajes))

tablapantalla <- data.frame(NOMBRE_LENGUAJE = unlist(listapantalla[3]),
		 					RATING_GITHUB = unlist(listapantalla[1]),
                 			NUMERO_APARICIONES = unlist(listapantalla[2])
                 )


#grafica

listagrafico <- insercion(unlist(repositorios),unlist(lenguajes))

par(mar=c(3, 15, 3, 10))

barplot(rev(unlist(listagrafico[1])),names.arg=rev(unlist(listagrafico[2])),beside = FALSE, horiz = TRUE, angle = 45,col="darkred",density=100, main="Numero de repositorios por lenguaje",border="black",las=1)

ubicacion = gsub("/","\\",ubicacion)

print(paste0("Se ha guardado un PDF con la grafica y un CSV con los resultados en: ",substring(current_filename(),1,punto-1)))
