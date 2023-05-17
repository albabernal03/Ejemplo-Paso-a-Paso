from contextlib import closing
import timeit
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys
from functools import partial
import asyncio
import aiohttp
import urllib.request

from urllib3 import HTTPConnectionPool
from urllib.error import URLError

from generador import download


#CON GENERADORES

def get_images_src_from_html(html_doc):    
    """Recupera todo el contenido de los atributos src de las etiquetas 
img"""   
    soup = BeautifulSoup(html_doc, "html.parser")    
    return (img.get('src') for img in soup.find_all('img'))     

def get_uri_from_images_src(base_uri, images_src):
    """Devuelve una a una cada URI de imagen a descargar"""  
    parsed_base = urlparse(base_uri)    
    for src in images_src:    
        parsed = urlparse(src)    
        if parsed.netloc == '':    
            path = parsed.path    
            if parsed.query:    
                path += '?' + parsed.query    
            if path[0] != '/':    
                if parsed_base.path == '/':    
                    path = '/' + path    
                else:    
                    path = '/' + '/'.join(parsed_base.path.split('/')[:-1]) + '/' + path    
            yield parsed_base.scheme + '://' + parsed_base.netloc + path    
        else:    
            yield parsed.geturl()

def wget(uri):
    try:
        response = urllib.request.urlopen(uri)
        if response.status == 200:
            print(response.reason, file=sys.stderr)
            return
        print('Respuesta OK')
        return response.read()
    except URLError as e:
        print("Error al abrir la URL:", e)

def get_image(page_uri):
    html= wget(page_uri)
    if not html:
       print('Error: no se ha encontado ninguna imagen', sys.stderr)
       return None
    images_scr_gen= get_images_src_from_html(html)
    images_uri_gen= get_uri_from_images_src(page_uri, images_scr_gen)
    for image_uri in images_uri_gen:
        print('Descarga de %s' % image_uri)
        download(image_uri)

if __name__ == '__main__':
    print('--- Descarga de imágenes ---')
    web_page_uri = 'https://www.formationpython.com/'
    print(timeit.timeit('get_image(web_page_uri)', number=10, setup='from __main__ import get_image, web_page_uri'))
