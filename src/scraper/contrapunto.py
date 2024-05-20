import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Base URL
base_url = "https://contrapunto.cl/3-categorias?page="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

# Function to scrape a single page
def scrape_page(page_number):
    url = f"{base_url}{page_number}"
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        print("Access denied to page", page_number)
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the book items on the page
    books = soup.find_all("div", class_="js-product-miniature-wrapper")
    
    # Extract book details
    book_list = []
    for book in books:
        title = book.find("h3").get_text(strip=True)
        author = book.find("div", class_="product-brand").get_text(strip=True) if book.find("div", class_="product-brand") else "N/A"
        price = book.find("span", class_="product-price").get_text(strip=True) if book.find("span", class_="product-price") else "N/A"
        price = re.sub("[^\d]", "", price)
        link = book.find("a")["href"]
        isbn = book.find("div", class_="product-reference").get_text(strip=True).replace("-", "") if book.find("div", class_="product-reference") else "N/A"
        book_list.append({"Title": title, "Author": author, "Price": price, "Link": link, "ISBN": isbn})
    
    return book_list

# Function to scrape all pages
def scrape_all_pages():
    all_books = []
    old_books = []
    page_number = 1
    
    while True:
        if page_number % 10 == 0:
            print("Scraping page", page_number)
        books = scrape_page(page_number)
        # Check if the books are the same as the previous page using the ISBN
        isbn = set(book["ISBN"] for book in books)
        old_isbn = set(book["ISBN"] for book in old_books)
        if isbn == old_isbn:
            print("No new books found on page", page_number)
            break
        if not books:
            break
        all_books.extend(books)
        page_number += 1
        old_books = books
    
    return all_books

# Scrape all books and store in a DataFrame
books = scrape_all_pages()
books_df = pd.DataFrame(books)

# Save to CSV
books_df.to_csv("librerias/contrapunto.csv", index=False)
print("Books data has been saved to contrapunto.csv")
