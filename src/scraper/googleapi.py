import csv
import requests
import sys

class CsvSaver:
	def __init__(self, inputfile: str,  filename: str):
		self.output_file_name = filename
		self.input_file_name = inputfile

	def check_if_book_is_present_in_google_api(self, output_file_name: str, row) -> bool:
		with open(output_file_name, newline='', encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile)
			data = list(reader)

			if len(data) <= row:
				return True

			interestedRow = data[row]
			return any(cell != '' for cell in interestedRow[5:9])

	def extract_data_google_api(self):
		try:
			with open(self.input_file_name, newline='', encoding='utf-8') as csvfile:
				reader = csv.reader(csvfile)
				data = list(reader)
				dataToSave = []
				i = 1
				count=0
				for row in data[1:]:
					if self.check_invalid_data(row):
						continue

					if self.check_if_book_is_present_in_google_api(self.output_file_name, i):
							isbn = row[4]
							extra_data = self.search_google_api(isbn)
							dataToSave.append(row + [extra_data['description'], extra_data['publishedDate'],
																			 extra_data['img'], extra_data['categories'],
																			 extra_data['avgRating'], extra_data['ratingsCount']])
							if extra_data['avgRating'] or extra_data['ratingsCount']:
								count+=1
					else:
						dataToSave.append(row + [None, None, None, None, None, None])
					i += 1
				print('Cantidad de libros con rating:', count)
				return dataToSave

		except FileNotFoundError:
			return 1

	def check_invalid_data(self, data: list) -> bool:
		return 'N/A' in data

	def search_google_api(self, isbn: str) -> dict:
		url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
		response = requests.get(url)
		book_data = response.json()

		if book_data.get('totalItems', 0) == 0:
			return {
				'description': None,
				'publishedDate': None,
				'img': None,
				'categories': None,
				'avgRating': None,
				'ratingsCount': None
			}

		book_data = book_data['items'][0]['volumeInfo']
		description = book_data.get('description', None)
		publishDate = book_data.get('publishedDate', None)
		img = book_data.get('imageLinks', None)
		categories = book_data.get('categories', None)
		avgRating = book_data.get('averageRating', None)
		ratingsCount = book_data.get('ratingsCount', None)

		if img:
			img = img.get('thumbnail', None)

		return {
			'description': description,
			'publishedDate': publishDate,
			'img': img,
			'categories': categories,
			'avgRating': avgRating,
			'ratingsCount': ratingsCount
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
			'AvgRating',
			'RatingsCount'
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
