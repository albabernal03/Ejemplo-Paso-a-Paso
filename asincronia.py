#En primer lugar vamos a descargar las librerías 
import asyncio #asyncio es la libreria principal de la programaión asíncrona y se utiliza para crear tareas asíncronas
import aiohttp #aiohttp es una librería que permite realizar peticiones HTTP de forma asíncrona
from bs4 import BeautifulSoup #BeautifulSoup es una librería que permite extraer datos de archivos HTML y XML
from urllib.parse import urlparse #urllib.parse es una librería que permite analizar y construir URLs
import sys #sys es una librería que permite acceder a variables y funciones mantenidas por el intérprete
from functools import partial #functools es una librería que permite trabajar con funciones y objetos invocables

async def wget(session, url): #async def define una función asíncrona
    async with session.get(url) as response: #async with permite ejecutar una función asíncrona dentro de otra
        if response.status != 200: #Si el estado de la respuesta no es 200, es decir, si no es correcto, se devuelve un error
            return None 
        if response.content_type.startswith('text/'): #Si el tipo de contenido de la respuesta es texto, se devuelve el texto
            return await response.text()
        else: #Si el tipo de contenido de la respuesta no es texto, se devuelve el contenido
            return await response.read()
        
async def download(session,uri): #Función que descarga el contenido de una url
    content = await wget(session,uri) 
    if content is None:
        return None
    sep = "/" if "/" in uri else "\\" #definimos el separador de la ruta
    with open(uri.split(sep)[-1], "wb") as f:  #abrimos el archivo en modo escritura binaria
        f.write(content)  
        return uri 
    

async def get_images_src_from_html(html_doc): #Función que obtiene las imágenes de un documento HTML
    soup = BeautifulSoup(html_doc, "html.parser")  #Creamos un objeto BeautifulSoup a partir del documento HTML, um objeto BeautifulSoup es un árbol que representa el documento HTML
    for img in soup.find_all('img'):  #Recorremos todas las etiquetas img del documento HTML
        yield img.get('src')  #Obtenemos el atributo src de la etiqueta img
        await asyncio.sleep(0.001) #Esperamos 0.001 segundos


async def get_uri_from_images_src(base_uri, images_src): #Función que obtiene la URI de las imágenes
    """Devuelve una a una cada URI de imagen a descargar"""  
    parsed_base = urlparse(base_uri)  #Analizamos la URI base
    async for src in images_src:  #Recorremos todas las URI de las imágenes
        parsed = urlparse(src)  
        if parsed.netloc == '':  #Si la URI no tiene netloc, es decir, no tiene dominio, se construye la URI completa
            path = parsed.path  #Obtenemos el path de la URI
            if parsed.query: #Si la URI tiene query, es decir, tiene parámetros, se añaden a la URI  
                path += '?' + parsed.query  
            if path[0] != '/':  #Si el primer carácter del path no es /, se añade
                if parsed_base.path == '/':
                    path = '/' + path  
                else:  
                    path = '/' + '/'.join(parsed_base.path.split('/')[:-1]) + '/' + path  #Si el path de la URI base no es /, se añade el path de la URI base a la URI 
            yield parsed_base.scheme + '://' + parsed_base.netloc + path  
        else:  
            yield parsed.geturl()  
        await asyncio.sleep(0.001) 



async def get_images(session, page_uri):   #Función que obtiene las imágenes de una página
    html = await wget(session, page_uri)  
    if not html:  
        print("Error: no se ha encontrado ninguna imagen", sys.stderr)  
        return None  
    images_src_gen = get_images_src_from_html(html)  
    images_uri_gen = get_uri_from_images_src(page_uri, images_src_gen)  
    async for image_uri in images_uri_gen:  
        print('Descarga de %s' % image_uri)  
        await download(session, image_uri) 


async def main(): #Función principal
    web_page_uri = 'http://www.formation-python.com/'  
    async with aiohttp.ClientSession() as session:  
        await get_images(session, web_page_uri) 

def write_in_file(filename, content):   #Función que escribe en un archivo
    with open(filename, "wb") as f:   
        f.write(content) 

async def download(session, uri):  
    content = await wget(session, uri)  
    if content is None:  
        return None  
    loop = asyncio.get_running_loop()  
    sep = "/" if "/" in uri else "\\"
    await loop.run_in_executor(None, partial(write_in_file, uri.split(sep)[-1], content))  
    return uri 

if __name__ == '__main__':  
    asyncio.run(main())

    