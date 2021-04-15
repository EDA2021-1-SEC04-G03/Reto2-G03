"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printLine():
    print('-------------------------------------')

def printMenu():
    printLine()
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los videos con más views por país y categoría")
    print("3- Consultar el video que más dias ha sido trending por país")
    print('4- Consultar el video mas trending por categoria')
    print('5- Consultar los n videos con mas likes por Pais y Tag')
    print("0- Salir")
    printLine()

def printMenuMapa():
    print("Seleccione el tipo de mapa que quiere crear:")
    print("1- Probing")
    print("2- Chaining")

def obtenerTipoMapa():
    iterate=True
    while iterate:
        printMenuMapa()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            tipo_mapa='PROBING'
            iterate=False
        elif int(inputs[0]) == 2:
            tipo_mapa='CHAINING'
            iterate=False
    return tipo_mapa

cont = None

"""
Menu principal
"""
running = True
while running:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:

        print("Cargando información de los archivos ....")

        cont = controller.initCatalog('PROBING', 0.5)
        answer = controller.loadData(cont)
        print('Videos cargados: ' + str(controller.videosSize(cont)))
        print('Categorías de los videos: ' + str(controller.categoriesSize(cont)))
        print('Paises de los videos: ' + str(controller.countriesSize(cont)))
        print('Categorías cargadas: ' + str(controller.categoriesListSize(cont)))

    elif int(inputs[0]) == 2:
        #req 1
        size=0
        category_name = input("Indique la categoría de los videos a consultar: ")
        country = input("Indique el país de los videos a consultar: ")
        id=controller.getIDbyCategoryName(cont, category_name)

        videosByCat=controller.getVideosByCategory(cont, id)

        filteredList=controller.filterVideos(videosByCat, ['country'],[country])

        while size<1 or size>lt.size(filteredList['videos']):
            size = int(input("Indique el número de videos a listar: "))

        print("Ordenando datos...\n")
        result = controller.sortVideos(filteredList, size, 'views')

        print('Videos top {} para {} bajo la categoría {}:\n'.format(size,country,category_name))

        print("trending_date | title | channel_title | publish_time | views | likes | dislikes")
        for i in lt.iterator(result):
            print(i['trending_date'],'|',i['title'],'|',i['channel_title'],'|',
            i['publish_time'],'|',i['views'],'|',i['likes'],'|',i['dislikes'])

    elif int(inputs[0]) == 3:
        #Req 2
        size=1
        country = input("Indique el país de los videos a consultar: ")
        
        videosByCountry=controller.getVideosByCountry(cont, country)

        print("Ordenando datos...\n")

        organizedList = controller.sortVideos(videosByCountry, None, 'title')

        result = controller.getTopVideoByTrendingDate(organizedList)

        print('El video top trending para {} es:\n'.format(country))
        
        print("title | channel_title | country | Días")
        print(result[0]['title'],'|',result[0]['channel_title'],'|',result[0]['country'],'|',result[1])

    elif int(inputs[0]) == 4:
        #req 3
        cat = input("Categoria:")

        result = controller.trendingByCat(cont,cat)

        print("title | channel_title | Category_ID | Días")
        print(result[0]['title'],'|',result[0]['channel_title'],'|',result[0]['category_id'],'|',result[1])
    
    elif int(inputs[0]) == 4:
        #req 3
        cat = input("Categoria:")

        result = controller.trendingByCat(cont,cat)

        print("title | channel_title | Category_ID | Días")
        print(result[0]['title'],'|',result[0]['channel_title'],'|',result[0]['category_id'],'|',result[1])

    elif int(inputs[0]) == 5:
        #req 4
        tag = input("Tag: ")
        country = input('Pais: ')
        Nvids = int(input('Cuantos videos: '))
        print('Cargando...')
        result = controller.searchByTag(cont, Nvids, tag, country)

        print("done")
        print('Los {} video(s) con mas likes para {} tag en {} es:\n'.format(Nvids, tag, country))
        for i in result['elements']:
            print("title | channel_title | Dia de publicacion | views | likes | dislikes | tags")
            print(i['title'],'|',i['channel_title'],'|',i['publish_time'],'|',i['views'],'|', 
                  i['likes'],'|',i['dislikes'],'|',i['tags'].split('|'))

    elif int(inputs[0]) == 0:
        running = False
        print("Adios!")


sys.exit(0)
