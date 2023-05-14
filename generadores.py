#En primer lugar vamos a descargar las librerías 
import asyncio #asyncio es la libreria principal de la programaión asíncrona y se utiliza para crear tareas asíncronas
import aiohttp #aiohttp es una librería que permite realizar peticiones HTTP de forma asíncrona
from bs4 import BeautifulSoup #BeautifulSoup es una librería que permite extraer datos de archivos HTML y XML

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