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
 """

from os import name
import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog(mapType, loadFactor):
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog(mapType, loadFactor)
    return catalog


# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """

    # TODO: modificaciones para medir el tiempo y memoria
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadVideos(catalog)
    loadCategory(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory

def loadVideos(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    videosfile = cf.data_dir + 'videos/videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)

def loadCategory(catalog):
    """
    Carga las categorias de videos y los agrega a la lista de categorías
    """
    categoryfile = cf.data_dir + 'videos/category-id.csv'
    input_file = csv.DictReader(open(categoryfile, encoding='utf-8'))
    for category in input_file:
        model.addCategoryList(catalog, category)

#Funciones de filtración

def filterVideos(catalog, fields, criterias):
    """
    Filtra los videos basados en un criterio para cada campo
    """
    return model.filterVideos(catalog, fields,criterias)

# Funciones de ordenamiento

def getTopVideoByTrendingDate(catalog):
    """
    Ordena los libros por average_rating
    """
    return model.getTopVideoByTrendingDate(catalog)

def sortVideos(catalog, size, criteria):
    """
    Ordena los libros por average_rating
    """
    return model.sortVideos(catalog, size, criteria)

# Funciones de consulta sobre el catálogo

def getVideosByCategory(catalog, catid):

    return model.getVideosByCategory(catalog, catid)

def getVideosByCountry(catalog, country):

    return model.getVideosByCountry(catalog, country)

def getIDbyCategoryName(catalog, catname):
    """
    Numero de libros cargados al catalogo
    """
    return model.getIDbyCategoryName(catalog, catname) 

def videosSize(catalog):
    """
    Numero de libros cargados al catalogo
    """
    return model.videosSize(catalog)

def categoriesSize(catalog):
    """
    Numero de autores cargados al catalogo
    """
    return model.categoriesSize(catalog)

def countriesSize(catalog):
    """
    Numero de autores cargados al catalogo
    """
    return model.countriesSize(catalog)

def categoriesListSize(catalog):
    """
    Numero de autores cargados al catalogo
    """
    return model.categoriesListSize(catalog)


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory


def trendingByCat (catalog, category):
    catId = model.getIDbyCategoryName(catalog, category)
    vidsInCat = model.getVideosByCategory(catalog, catId)
    vidsSorted = model.sortVideos(vidsInCat,None,'title')
    topVid = model.getTopVideoByTrendingDate(vidsSorted)

    return topVid

def searchByTag(catalog, videos, tag, country):
    '''
    Busca N videos con un tag especifico en un pais
    '''
    tag = '"'+tag+'"'
    vidsCountry = model.getVideosByCountry(catalog,country)
    vidsConTag = model.filterVidsByTag(vidsCountry,tag)
    result = model.sortVideos(vidsConTag,videos,'likes')
    print(result)
    return result