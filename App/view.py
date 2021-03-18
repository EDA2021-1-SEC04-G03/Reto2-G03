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

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los videos con más views por país y categoría")

cont = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        
        print("Cargando información de los archivos ....")
        cont = controller.initCatalog()
        controller.loadData(cont)
        print('Videos cargados: ' + str(controller.videosSize(cont)))
        print('Categorías de los videos: ' + str(controller.categoriesSize(cont)))
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

    else:
        sys.exit(0)
sys.exit(0)
