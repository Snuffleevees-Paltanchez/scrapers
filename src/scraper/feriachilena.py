import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Base URL
base_url = "https://feriachilenadellibro.cl/page/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

# Function to scrape a single page
def scrape_page(page_number):
    url = f"{base_url}{page_number}/?post_type=product"
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        print("Access denied to page", page_number)
        return []
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the book items on the page
    books = soup.find_all("li", class_="product-type-simple")

    # Extract book details
    book_list = []
    for book in books:
        title = book.find("h2").get_text(strip=True)
        link = book.find("a", class_="ast-loop-product__link")["href"]

        response2 = requests.get(link, headers=headers)
        if response2.status_code == 403:
            print("Access denied to title", title)
            continue
        soup2 = BeautifulSoup(response2.content, "html.parser")

        short_desc_div = soup2.find(
            "div", class_="woocommerce-product-details__short-description"
        )
        # Extract the author
        author = None
        if short_desc_div:
            text = short_desc_div.get_text(separator="\n")
            for line in text.split("\n"):
                if "Autor:" in line:
                    author = line.replace("Autor:", "").strip()
                    author = reformat_name(author)
                    break
        if not author:
            print("Author not found for", title)
            author = "N/A"

        price = book.find("bdi").get_text(strip=True) if book.find("bdi") else "N/A"
        price = re.sub("[^\d]", "", price)
    
        isbn = (
            soup2.find("span", class_="sku").get_text(strip=True)
            if soup2.find("span", class_="sku")
            else "N/A"
        )

        book_list.append(
            {
                "Title": title,
                "Author": author,
                "Price": price,
                "Link": link,
                "ISBN": isbn,
            }
        )

    return book_list


# Function to scrape all pages
def scrape_all_pages():
    all_books = []
    page_number = 1

    while True:
        if page_number % 10 == 0:
            print("Scraping page", page_number)
        books = scrape_page(page_number)
        if not books:
            break
        all_books.extend(books)
        page_number += 1

    return all_books

def reformat_name(name):
    return ' '.join(reversed(name.title().split(', ')))

# Scrape all books and store in a DataFrame
books = scrape_all_pages()
books_df = pd.DataFrame(books)

# Save to CSV
books_df.to_csv("librerias/feriachilena.csv", index=False)
print("Books data has been saved to feriachilena.csv")
