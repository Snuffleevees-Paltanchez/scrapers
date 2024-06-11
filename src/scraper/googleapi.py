import csv
import requests
import sys

class CsvSaver:
    def __init__(self, inputfile: str,  filename: str):
        self.output_file_name = filename
        self.input_file_name = inputfile

    def extract_data_google_api(self):
        try:
            with open(self.input_file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                dataToSave = []
                for row in data[1:]:
                    if self.check_invalid_data(row):
                        continue

                    isbn = row[4]
                    extra_data = self.search_google_api(isbn)
                    dataToSave.append(row + [extra_data['description'], extra_data['publishedDate'], extra_data['img'], extra_data['categories']])
                return dataToSave
        except FileNotFoundError:
            return 1
    
    def check_invalid_data(self, data: list) -> bool:        
        if 'N/A' in data:
            return True
        
        return False

        
    def search_google_api(self, isbn: str) -> dict:
        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
        response = requests.get(url)
        book_data = response.json()


        if book_data.get('totalItems', 0) == 0:
            return {
                'description': None,
                'publishedDate': None,
                'img': None,
                'categories': None
            }

        book_data = book_data['items'][0]['volumeInfo']
        description = book_data.get('description', None)
        publishDate = book_data.get('publishedDate', None)
        img = book_data.get('imageLinks', None)
        categories = book_data.get('categories', None)

        if img:
            img = img.get('thumbnail', None)

        return {
            'description': description,
            'publishedDate': publishDate,
            'img': img,
            'categories': categories
        }


    def save_data(self, data: list) -> None:
        header = [
            'Title',
            'Author',
            'Price',
            'Link',
            'ISBN', 
            'Description',
            'PublishedDate', 
            'ImgUrl', 
            'Categories'
        ]
        with open(self.output_file_name, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(header)
            writer.writerows(data)


if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    csvsaver = CsvSaver(inputfile, outputfile)
    data = csvsaver.extract_data_google_api()
    if data:
        csvsaver.save_data(data)
