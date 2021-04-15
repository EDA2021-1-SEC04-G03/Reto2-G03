"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(tipoMapa, factorCarga):

    catalog = {'videos': None,
               'category': None,
               'country': None,
               'category_id': None}


    catalog['videos'] = lt.newList('SINGLE_LINKED')

    catalog['category_id'] = lt.newList('SINGLE_LINKED')

    catalog['category'] = mp.newMap(40,
                                   maptype=tipoMapa,
                                   loadfactor=factorCarga,
                                   comparefunction=None)

    catalog['country'] = mp.newMap(15,
                                   maptype=tipoMapa,
                                   loadfactor=factorCarga,
                                   comparefunction=None)

    return catalog

# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    """
    Se adiciona un video a la lista de videos
    """
    lt.addLast(catalog['videos'], video)
    addCategory(catalog, video['category_id'], video)
    addCountry(catalog, video['country'], video)

def addCategory(catalog, category_id, video):
    """
    Esta función adiciona un video a la lista de videos de la misma categoría.
    """
    categories = catalog['category']
    existcat = mp.contains(categories, category_id)
    if existcat:
        entry = mp.get(categories, category_id)
        category = me.getValue(entry)
    else:
        category = newCategory(category_id)
        mp.put(categories, category_id, category)
    lt.addLast(category['videos'], video)

def addCountry(catalog, country, video):
    """
    Esta función adiciona un video a la lista de videos de la misma categoría.
    """
    countries = catalog['country']
    existcountry = mp.contains(countries, country)
    if existcountry:
        entry = mp.get(countries, country)
        countrybean = me.getValue(entry)
    else:
        countrybean = newCountry(country)
        mp.put(countries, country, countrybean)
    lt.addLast(countrybean['videos'], video)

def addCategoryList(catalog, category):
    """
    Adiciona una categoria a la lista de categorias
    """
    category_fixed=category['id\tname'].replace('\t','').split(" ",1)
    c = newListCategory(category_fixed[1], category_fixed[0])
    lt.addLast(catalog['category_id'], c)

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByViews(video1, video2):
    """ Devuelve verdadero (True) si los 'views' de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'views'
        video2: informacion del segundo video que incluye su valor 'views'
    """
    return (int(video1['views']) > int(video2['views']))

def cmpVideosByTitle(video1, video2):
    """ Devuelve verdadero (True) si los 'title' de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'title'
        video2: informacion del segundo video que incluye su valor 'title'
    """
    return (video1['title']) < (video2['title'])

def cmpVideosByLikes(video1, video2):
    """ Devuelve verdadero (True) si los 'likes' de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'likes'
        video2: informacion del segundo video que incluye su valor 'likes'
    """
    return (int(video1['likes']) > int(video2['likes']))

# Funciones para creacion de datos

def newListCategory(name, id):
    """
    Esta estructura almacena las categorias utilizados para marcar videos.
    """
    category = {'name': '', 'id': ''}
    category['name'] = name
    category['id'] = id
    return category

def newCategory(name):
    """
    Crea una nueva estructura para modelar los videos de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    category = {'name': "",
              "videos": None}
    category['name'] = name
    category['videos'] = lt.newList('ARRAY_LIST', None)
    return category

def newCountry(name):
    """
    Crea una nueva estructura para modelar los videos de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    country = {'name': "",
              "videos": None}
    country['name'] = name
    country['videos'] = lt.newList('ARRAY_LIST', None)
    return country

#Funciones de filtración

def filterVideos(catalog, fields, criterias):
    """ Filtra los videos basados en sus campos y en los valores aceptados por los mismos.
    Si fields es (field1, field2) y criterias es (criteria1, criteria2) entonces la función retornará
    una lista en la que sólo field1 tenga el valor criteria1, y así sucesivamente.
    Args:
        fields(list): campos usados para la filtración
        criterias(list): valores posibles para los campos
    """

    newCatalog = {'videos': None}

    newCatalog['videos'] = lt.newList('ARRAY_LIST')

    for video in lt.iterator(catalog['videos']):
        add=True
        for i in range(len(fields)):
            if video[fields[i]] != criterias[i]:
                add=False
                break
        if add:
            lt.addLast(newCatalog['videos'], video)

    return newCatalog

# Funciones de consulta

def getVideosByCategory(catalog, catid):
    entry = mp.get(catalog['category'], catid)
    return me.getValue(entry)

def getVideosByCountry(catalog, country):
    entry = mp.get(catalog['country'], country)
    return me.getValue(entry)
    

def getIDbyCategoryName(catalog, catname):
    catid=-1
    for category in lt.iterator(catalog['category_id']):
        if category['name']==catname:
            catid=category['id']
            break
    return catid

def videosSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['videos'])

def categoriesListSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['category_id'])

def categoriesSize(catalog):
    """
    Numero de autores en el catalogo
    """
    return mp.size(catalog['category'])

def countriesSize(catalog):
    """
    Numero de autores en el catalogo
    """
    return mp.size(catalog['country'])

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def getTopVideoByTrendingDate(catalog):
    tempElement=lt.firstElement(catalog)
    topElemento=None
    contTopElement=0
    contador=0
    
    for elemento in lt.iterator(catalog):
        if elemento['video_id']==tempElement['video_id']:
            contador+=1
        else:
            if contador>contTopElement:
                topElemento=tempElement
                contTopElement=contador
            contador=1
            tempElement=elemento
    
    if contador>contTopElement:
        topElemento=tempElement
        contTopElement=contador

    return (topElemento,contTopElement)

def sortVideos(catalog, size, criteria):

    if criteria=='views':
        sorted_list = ms.sort(catalog['videos'], cmpVideosByViews)
    elif criteria=='title':
        sorted_list = ms.sort(catalog['videos'], cmpVideosByTitle)
    elif criteria == 'likes':
        sorted_list = ms.sort(catalog['videos'], cmpVideosByLikes)

    if criteria=='views' or criteria=='likes':
        sorted_list = lt.subList(sorted_list, 1, size)

    return sorted_list