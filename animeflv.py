import requests
from lxml import html

encabezados = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"}

url = "https://www3.animeflv.net"
url_browse = "https://www3.animeflv.net/browse"

datos_animes = []
pagina_actual = 1
max_paginas = 2  # Limitar el número de páginas a recorrer
#respuesta = requests.get(url, headers=encabezados)
respuesta = requests.get(url_browse, headers=encabezados)

while pagina_actual <= max_paginas:
    # Actualizar la URL con el número de página
    url_pagina = f"{url_browse}?page={pagina_actual}"
    print(f"Extrayendo datos de la página: {pagina_actual}")
    
    #respuesta = requests.get(url, headers=encabezados)
    respuesta = requests.get(url_pagina, headers=encabezados)

    if respuesta.status_code == 200:
        parser = html.fromstring(respuesta.content)

        """ nombres_animes = parser.xpath("//ul[@class='ListAnimes AX Rows A06 C04 D03']//article[contains(@class, 'Anime')]//h3[@class='Title']/text()")
        urls_imagenes = parser.xpath("//ul[@class='ListAnimes AX Rows A06 C04 D03']//article[@class='Anime alt B']//img/@src") """
        #urls_links = parser.xpath("//ul[@class='ListAnimes AX Rows A06 C04 D03']//article[@class='Anime alt B']//a/@href")
        urls_links = parser.xpath("//ul[@class='ListAnimes AX Rows A03 C02 D02']/li/article[@class='Anime alt B']/a/@href")



        
        """ for nombre, url_imagen, url_link in zip(nombres_animes, urls_imagenes, urls_links): """
        for url_link in(urls_links):
            """ print("Nombre del anime:", nombre)
            print("URL de la imagen:", url+url_imagen) """
            print("URL del link:", url+url_link)
            
            
            
            # Hacer una solicitud a la página de cada anime para obtener más detalles
            url_anime = url + url_link
            respuesta_anime = requests.get(url_anime, headers=encabezados)
            
            if respuesta_anime.status_code == 200:
                # Parsear la página de detalles del anime
                parser_anime = html.fromstring(respuesta_anime.content)

                titulo = parser_anime.xpath("//div[@class='Ficha fchlt']//div[@class='Container']//h1[@class='Title']/text()")
                titulo = titulo[0].strip() if titulo else "N/A"

                tipo_anime = parser_anime.xpath("//div[@class='Ficha fchlt']//div[@class='Container']//span[@class='Type tv']/text()")
                tipo_anime = tipo_anime[0].strip() if tipo_anime else "N/A"

                anime_cover = parser_anime.xpath("//aside[@class='SidebarA BFixed']/div[@class='AnimeCover']/div[@class='Image']//img/@src")
                anime_cover = anime_cover[0].strip() if anime_cover else "N/A"
                    
                anime_status = parser_anime.xpath("//aside[@class='SidebarA BFixed']/p[@class='AnmStts']/span[@class='fa-tv']/text()")
                anime_status = anime_status[0].strip() if anime_status else "N/A"

                # Extraer la sinopsis del anime (esto depende de la estructura HTML de la página)
                sinopsis = parser_anime.xpath("//section[@class='WdgtCn']/div[@class='Description']/p/text()")
                sinopsis = sinopsis[0].strip() if sinopsis else "N/A"

                # Extraer géneros del anime
                generos = parser_anime.xpath("//section[@class='WdgtCn']/nav[@class='Nvgnrs']/a/text()")
                lista_generos = [genero.strip() for genero in generos] if generos else ["N/A"]

                """ # Extraer otros detalles, como episodios o estado (opcional)
                episodios = parser_anime.xpath("//span[contains(text(), 'Episodios')]/following-sibling::strong/text()")
                if episodios:
                    print("Episodios:", episodios[0]) """
                    
                datos_animes.append({
                    "Titulo": titulo,
                    "Tipo anime": tipo_anime,
                    "Cover": url + anime_cover,
                    "Status": anime_status,
                    "Sinopsis": sinopsis,
                    "Géneros": ', '.join(lista_generos)
                })

            else:
                print(f"Error al acceder a los detalles del anime en: {url_anime}. Código de estado: {respuesta_anime.status_code}")
        pagina_actual += 1  # Pasar a la siguiente página
            
        # Imprimir todos los detalles de los animes
        # Verifica que los datos estén presentes
        
    else:
        print("Error al obtener la página web. Código de estado:", respuesta.status_code)
        
if datos_animes:  # Comprueba que la lista no esté vacía
    for anime in datos_animes:
        for key, value in anime.items():
            print(f"{key}: {value}")
        print("=" * 40)  # Separador de 40 signos de igual
    else:
        print("No hay datos en la lista.")
print(type(datos_animes))