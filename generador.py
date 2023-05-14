
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys
from functools import partial
import asyncio
import aiohttp
import urllib.request

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

def wget(session, uri):
    """Devuelve el contenido de una URI"""  
    try:    
        with session.get(uri) as response:    
            if response.status == 200:    
                return response.content    
            else:    
                print("Error: %s" % response.status, sys.stderr)    
                return None    
    except Exception as e:    
        print("Error: %s" % e, sys.stderr)    
        return None
    
def download(session, uri):
    """Descarga una URI"""  
    content = wget(session, uri)    
    if content is None:    
        return None    
    sep = "/" if "/" in uri else "\\"    
    with open(uri.split(sep)[-1], "wb") as f:    
        f.write(content)


def get_images(session, page_uri):
    """Recupera todas las imágenes de una página"""  
    html = wget(session, page_uri)    
    if not html:    
        print("Error: no se ha encontrado ninguna imagen", sys.stderr)    
        return None    
    images_src_gen = get_images_src_from_html(html)    
    images_uri_gen = get_uri_from_images_src(page_uri, images_src_gen)    
    for image_uri in images_uri_gen:    
        print('Descarga de %s' % image_uri)    
        download(session, image_uri)

def main():
    """Función principal"""  
    if len(sys.argv) < 2:    
        print("Error: falta la URI de la página", sys.stderr)    
        return 1    
    page_uri = sys.argv[1]    
    with aiohttp.ClientSession() as session:    
        get_images(session, page_uri)    
    return 0

if __name__ == "__main__":
    main()
    

