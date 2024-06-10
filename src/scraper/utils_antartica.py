import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import csv

links = [
        "https://www.antartica.cl/", "https://www.antartica.cl/libros.html",
        "https://www.antartica.cl/libros/arte-y-arquitectura.html",
        "https://www.antartica.cl/libros/ciencias.html",
        "https://www.antartica.cl/libros/ciencias-exactas.html",
        "https://www.antartica.cl/libros/ciencias-humanas.html",
        "https://www.antartica.cl/libros/computacion-e-informacion.html",
        "https://www.antartica.cl/libros/cuerpo-y-mente.html",
        "https://www.antartica.cl/libros/economia-y-administracion.html",
        "https://www.antartica.cl/libros/entretencion-y-manual.html",
        "https://www.antartica.cl/libros/gastronomia-y-vinos.html",
        "https://www.antartica.cl/libros/guias-de-viaje-y-tur.html",
        "https://www.antartica.cl/libros/infantil-y-juvenil.html",
        "https://www.antartica.cl/libros/literatura.html",
        "https://www.antartica.cl/libros/mundo-comic.html"
    ]


def get_all_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = set()
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                # Convertir URL relativa a absoluta
                full_url = urljoin(url, href)
                links.add(full_url)
            return links
        else:
            return set()
    except Exception as e:
        print(f"Error al obtener enlaces de {url}: {e}")
        return set()

def scrap(books, dict_books):
    for book in books:
        try:
            name = book.find("a", class_="product-item-link").text.strip()
            if name in dict_books:
                print(f'El libro {name} ya existe\n')
            else:
                price = book.find("span", class_="price-wrapper").text.strip()
                author = book.find("a", class_="link-autor-search-result").text.strip()
                href = book.find("a", class_="product-item-photo")["href"]
                # img = book.find("img", class_="product-image-photo")["src"]
                dict_books[name] = [price, author, href]
        except Exception as e:
            print(f'Error: {e}\n')

def fetch_page(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f'Error al obtener la página {link}: {e}')
        return None

def search_for_books(links, dict_books, max_pages, max_workers):
    count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_page, link): link for link in links}

        for future in as_completed(future_to_url):
            page = future.result()
            if page:
                soup = BeautifulSoup(page, "html.parser")
                books = soup.find_all("li", class_="product-item")
                scrap(books, dict_books)

                next_page = soup.find("a", class_="next-page")
                if next_page and count < max_pages:
                    next_page_link = next_page["href"]
                    if next_page_link != "javascript:void(0)":
                        next_page_link = urljoin(future_to_url[future], next_page_link)
                        print(f'Siguiente página: {next_page_link}')
                        search_for_books([next_page_link], dict_books, 1, 10)

                count += 1
                if count >= max_pages:
                    break

def create_csv(dict_books):     
    with open('librerias/antartica.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Titulo', 'Autor', 'Precio', 'Link', 'ISBN'])
        for name, details in dict_books.items():
            writer.writerow([name, details[1], details[0], details[2], details[3]])


def search_isbn(dict_books):
    
    for book in dict_books:
        try:
            # https://www.antartica.cl/g3-honor-y-traicion-9789566239055.html
            href = dict_books[book][2]
            isbn = href.split('-')[-1].split('.')[0]
            print(f'ISBN: {isbn}')
            dict_books[book].append(isbn)
        except Exception as e:
            print(f'Error al obtener el ISBN: {e}')
    return dict_books
        



        