import requests
from bs4 import BeautifulSoup

def buscar_ml_palabra(palabra):
    url_ml = f"https://listado.mercadolibre.com.co/{palabra.replace(' ', '-')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    respuesta = requests.get(url_ml, headers=headers)
    
    if respuesta.status_code != 200:
        print("Ha ocurrido un error al acceder a MercadoLibre")
        exit()
        
    soup = BeautifulSoup(respuesta.text, "html.parser")
    
    items = soup.select(".ui-search-result__wrapper")[:5]
    
    print(f"Resultados para: {palabra}\n")
    for i, item in enumerate(items, 1):
        title_tag = item.select_one("a.poly-component__title")
        price_tag = item.select_one("span.andes-money-amount__fraction")

        title = title_tag.get_text(strip=True) if title_tag else "Sin título"
        price = price_tag.get_text(strip=True) if price_tag else "Sin precio"

        print(f"{i}. {title} - ${price}")
        
palabra_busqueda = input("Ingrese palabra de búsqueda: ")

buscar_ml_palabra(palabra_busqueda)