
from bs4 import BeautifulSoup


def get_images_src_from_html(html_doc):    
    """Recupera todo el contenido de los atributos src de las etiquetas 
img"""   
    soup = BeautifulSoup(html_doc, "html.parser")    
    return (img.get('src') for img in soup.find_all('img')) 
