import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from utils_antartica import get_all_links, scrap, search_for_books, links, create_csv


if __name__ == "__main__":
    url = "https://www.antartica.cl/"
    dict_books = {}

    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    books = soup.find_all("li", class_="product-item")
    scrap(books, dict_books)

    search_for_books(links, dict_books, 10, 10)

    print("Libros encontrados:")
    for name, details in dict_books.items():
        print(f"Nombre: {name}")
        print(f"Precio: {details[0]}")
        print(f"Autor: {details[1]}")
        print(f"Imagen: {details[2]}")
        print("")

    print(f'Cantidad de links encontrados: {len(links)}')
    print(f'Cantidad de libros scrapeados: {len(dict_books)}')

    ## create and save in csv
    create_csv(dict_books)
    print('CSV file created')
