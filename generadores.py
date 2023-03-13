#En primer lugar vamos a descargar las librerías 
import asyncio #asyncio es la libreria principal de la programaión asíncrona y se utiliza para crear tareas asíncronas
import aiohttp #aiohttp es una librería que permite realizar peticiones HTTP de forma asíncrona

async def main(uri): #esta función es la que se encarga de realizar la petición HTTP y lo hace de forma asincrona gracias a la palabra reservada async
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            if response.status != 200:
                return None
            if response.content_type.startswith('text/'):
                return await response.text()
            else:
                return await response.read()