#En primer lugar vamos a descargar las librerías 
import asyncio #asyncio es la libreria principal de la programaión asíncrona y se utiliza para crear tareas asíncronas
import aiohttp #aiohttp es una librería que permite realizar peticiones HTTP de forma asíncrona

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
    

    