
import requests
from lxml import html

encabezados = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"}

url = "https://www3.animeflv.net"



respuesta = requests.get(url, headers=encabezados)


if respuesta.status_code == 200:
    parser = html.fromstring(respuesta.content)

    nombres_animes = parser.xpath("//ul[@class='ListAnimes AX Rows A06 C04 D03']//article[contains(@class, 'Anime')]//h3[@class='Title']/text()")
    urls_imagenes = parser.xpath("//ul[@class='ListAnimes AX Rows A06 C04 D03']//article[@class='Anime alt B']//img/@src")
    urls_links = parser.xpath("//ul[@class='ListAnimes AX Rows A06 C04 D03']//article[@class='Anime alt B']//a/@href")



    
    for nombre, url_imagen, url_link in zip(nombres_animes, urls_imagenes, urls_links):
        print("Nombre del anime:", nombre)
        print("URL de la imagen:", url+url_imagen)
        print("URL del link:", url+url_link)
        
        
        
        # Hacer una solicitud a la página de cada anime para obtener más detalles
        url_anime = url + url_link
        respuesta_anime = requests.get(url_anime, headers=encabezados)
        
        if respuesta_anime.status_code == 200:
            # Parsear la página de detalles del anime
            parser_anime = html.fromstring(respuesta_anime.content)

            # Extraer la sinopsis del anime (esto depende de la estructura HTML de la página)
            sinopsis = parser_anime.xpath("//section[@class='WdgtCn']/div[@class='Description']/p/text()")
            if sinopsis:
                sinopsis = sinopsis[0].strip()
                print("Sinopsis:", sinopsis)

            # Extraer géneros del anime
            generos = parser_anime.xpath("//section[@class='WdgtCn']/nav[@class='Nvgnrs']/a/text()")
            # Verificamos si existen géneros
            if generos:
            # Almacenar la lista de géneros
                lista_generos = [genero.strip() for genero in generos]  # Limpiamos espacios en blanco innecesarios
            # Imprimir la lista de géneros
                print("Géneros:", ', '.join(lista_generos))
            else:
                print("No se encontraron géneros")

            """ # Extraer otros detalles, como episodios o estado (opcional)
            episodios = parser_anime.xpath("//span[contains(text(), 'Episodios')]/following-sibling::strong/text()")
            if episodios:
                print("Episodios:", episodios[0]) """

        else:
            print(f"Error al acceder a los detalles del anime en: {url_anime}. Código de estado: {respuesta_anime.status_code}")
        
        print("=" * 40)

else:
    print("Error al obtener la página web. Código de estado:", respuesta.status_code)