from utils_antartica import search_isbn

if __name__ == "__main__":
    dict_books = {}
    dict_books['honor']=['author', 'price', 'https://www.antartica.cl/g3-honor-y-traicion-9789566239055.html']
    print(dict_books)
    search_isbn(dict_books)
    print(dict_books)
