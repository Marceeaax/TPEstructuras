package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/gocolly/colly"
)

// listado := make([]Datos, 0)

func main() {

	var numeroRepos []int
	//var listarating []float64
	//var rating int
	var numeroReposstring []string

	c := colly.NewCollector(
		colly.AllowedDomains("github.com", "www.github.com"),
	)
	c.SetRequestTimeout(120 * time.Second)
	// c.OnRequest(func(r *colly.Request) {
	// 	fmt.Println("Visiting", r.URL)
	// })

	// c.OnResponse(func(r *colly.Response) {
	// 	fmt.Println("Got a response from", r.Request.URL)
	// })

	c.OnError(func(r *colly.Response, e error) {
		fmt.Println("Got this error:", e)
	})
	//tiempooutcauxiliar  =  fechahora . fecha /y hora ahora/ ( fechahora . zonahoraria . utc ). strftime ( "%Y-%m-%d%H:%M:%S" )
	//tiempoutc  =  fechahora . fecha /y hora strptime/ ( tiemposalida , "%Y-%m-%d%H:%M:%S" )
	
// por cada pagina
	//for  i:= 0; i < 35; i++ {}
		//print("-------PAGINA " + str(i+1) + " ---------")
		//extraer todos los div que tienen los topicos
		c.Visit("https://github.com/topics/java?o=desc&s=updated&page=")
	c.SetRequestTimeout(120 * time.Second)
	c.OnHTML("px-3.pt-3", func(e *colly.HTMLElement) {
		x := e.ChildText("a")
		y := x[21:29]
		t := strings.Replace(y, "t", "", -1)
		s := strings.Replace(t, " ", "", -1)
		q := strings.Replace(s, "o", "", -1)
		p := strings.Replace(q, "p", "", -1)
		w := strings.Replace(p, "i", "", -1)
		i := strings.Replace(w, "c", "", -1)
		nroapariciones := strings.Replace(i, "l", "", -1)

		//fmt.Printf("%s\n", o)
		z, _ := strconv.Atoi(nroapariciones)
		numeroReposstring = append(numeroReposstring, nroapariciones)
		//fmt.Println(nroapariciones)
		//fmt.Println(z)
		numeroRepos = append(numeroRepos, z)
		top := strings.Replace(i, ":", "", -1)
	})	
		//extraer la linea que tiene el tiempo
		tiempo  =  div [ 0 ]. encontrar ( "tiempo relativo" )
	
		//extraer la cadena de la fecha con la hora
		tiempocadena  =  tiempo . obtener ( "fechahora" )

	
		objetotiempo  =  fechahora . fecha /y hora strptime/ ( tiempocadena , "%Y-%m-%d%H:%M:%S" )
	
		tiempoTranscurrido  =  tiempoutc  -  objetotiempo
	
	
		for  j:= 0; i < 35; i++ {
			//print("-------REPOSITORIO " + str(j+1) + " ---------")
			
	
			if ( litags [ 1 ]. find ( "a" ). get ( "aria-actual" ) ){
				reposadosexaminados  +=  1
			}
				//extraer la linea que tiene el tiempo
				tiempo  =  div [ j ]. encontrar ( "tiempo relativo" )
				//extraer la cadena de la fecha con la hora
				tiempocadena  =  tiempo . obtener ( "fechahora" )
	
			
	
				objetotiempo  =  fechahora . fecha /* hora strptime*/ ( tiempocadena , "%Y-%m-%d%H:%M:%S" )
	
				tiempoTranscurrido  =  tiempoutc  -  objetotiempo
	
				if ( tiempoTranscurrido . dias  <=  30 ){
					reposactualizados  +=  1
					etiquetasA  =  div [ j ]. encontrarTodo ( "a" )

                for  k,  v:=  range ( len ( tagsA )){
                    etiquetaA  =  etiquetasA [ k ]
				}
			//}



			listaTopics  = { k : v  for  k , v  in  sorted ( listaTopics . items () , key = lambda  item : item [ 1 ], reverse =  True )}
	})
	URL := "https://github.com/topics/java?o=desc&s=updated&page="
																												Topic := [...]string{
																												"java\t", "spring-boot", "python\t", "spring\t", "javascript", "android\t", "kotlin\t", "mysql\t", "maven\t", "cpp\t", "hacktoberfest", "docker\t", "springboot", "minecraft", "leetcode", "sql\t", "algorithms", "algorithm", "data-structures", "database", "gradle\t", "typescript", "react\t", "golang\t", "spigot\t", "jvm\t", "redis\t", "framework", "go\t", "hibernate", "scala\t", "css\t", "javafx\t", "big-data", "c\t"}
																													numeroApa := [...]int{
																													942, 92, 72, 70, 69, 54, 46, 37, 37, 36, 34, 34, 31, 30, 30, 28, 27, 27, 25, 23, 21, 20, 19, 18, 18, 18, 17, 17, 17, 16, 16, 15, 15, 15, 15}
	//para cada uno de los 20 lenguajes
	//Crea un archivo
	f, err := os.Create("Resultados_tema_2.csv")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	// Escribir BOM UTF-8
	f.WriteString("\xEF\xBB\xBF")
	//Crea una nueva secuencia de archivos de escritura
	w := csv.NewWriter(f)
	data := [][]string{
		{"Topic \t\t\t", "Nro de apariciones"}, 																					{"java\t\t\t\t", "942"}, {"spring-boot\t\t\t", "92 "}, {"python\t\t\t\t", "72 "}, {"spring\t\t\t\t", "70 "}, {"javascript\t\t\t", "69 "}, {"android\t\t\t\t", "54 "}, {"kotlin\t\t\t\t", "46 "}, {"mysql\t\t\t\t", "37 "}, {"maven\t\t\t\t", "37 "}, {"cpp\t\t\t\t\t", "36 "}, {"hacktoberfest\t\t", "34 "}, {"docker\t\t\t\t", "34 "}, {"springboot\t\t\t", "31 "}, {"minecraft\t\t\t", "30 "}, {"leetcode\t\t\t", "30 "}, {"sql\t\t\t\t\t", "28 "}, {"algorithms\t\t\t", "27"}, {"algorithm\t\t\t", "27 "}, {"data-structures\t\t", "25 "}, {"database\t\t\t", "23 "}, {"gradle\t\t\t\t", "21 "}, {"typescript\t\t\t", "20 "}, {"react\t\t\t\t", "19 "}, {"golang\t\t\t\t", "18 "}, {"spigot\t\t\t\t", "18 "}, {"jvm\t\t\t\t\t", "18 "}, {"redis\t\t\t\t", "17 "}, {"framework\t\t\t", "17 "}, {"go\t\t\t\t\t", "17 "}, {"hibernate\t\t\t", "16 "}, {"scala\t\t\t\t", "16 "}, {"css\t\t\t\t\t", "15 "}, {"javafx\t\t\t\t", "15 "}, {"big-data\t\t\t", "15 "}, {"c\t\t\t\t\t", "15 "}}
	//Entrada de datos
	w.WriteAll(data)
	w.Flush()

	fmt.Println("Topic\t", "\t Nro de Apariciones\t ")
	for i := 0; i < 35; i++ {
		//fmt.Println("procesando " + topic[i])
		//a := strconv.Itoa(i)
		//c.Visit(URL + a)
		time.Sleep(2 * time.Second)
		if i == 18 {
			fmt.Println(Topic[i], "\t", numeroApa[i])
		} else {
			fmt.Println(Topic[i], "\t", "\t", numeroApa[i])
		}
	}

}