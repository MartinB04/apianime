
import requests
from lxml import html

encabezados = {"user-agents": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"}

url = "https://www3.animeflv.net"



respuesta = requests.get(url, headers=encabezados)


if respuesta.status_code == 200:
    parser = html.fromstring(respuesta.content)

    nombres_animes = parser.xpath("//ul[@class='ListAnimes AX Rows A06 C04 D03']//article[contains(@class, 'Anime')]//h3[@class='Title']/text()")
    urls_imagenes = parser.xpath("//ul[@class='ListAnimes AX Rows A06 C04 D03']//article[@class='Anime alt B']//img/@src")

    # urls_animes = parser.xpath("//div[@class='book-list']//a[@class='text-center']/img/@src")


    
    for nombre, url_imagen in zip(nombres_animes, urls_imagenes):
        print("Nombre del manga:", nombre)
        print("URL de la imagen:", url+url_imagen)
        

else:
    print("Error al obtener la página web. Código de estado:", respuesta.status_code)