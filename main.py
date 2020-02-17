import sys

libCatalog = dict()
fetchedResults = dict()
line_break = '-------------------------------------------'

def add_book(key, bookTitle, bookAuthor, bookReleaseDate, bookGenre, bookQuantity):
	libCatalog[key] = [bookTitle, bookAuthor, bookReleaseDate, bookGenre, bookQuantity]

def add_to_catalog():
	print(line_break)
	print('ADD BOOK\n')
	for i in range(1):
		key = input('Book ISBN: ')
		bookTitle = input('Book Title: ')
		bookAuthor = input('Book Author: ')
		bookReleaseDate = input('Book Release Date: ')
		bookGenre = input('Book Genre: ')
		bookQuantity = input('Book Quantity: ')

		add_book(key, bookTitle, bookAuthor, bookReleaseDate, bookGenre, bookQuantity)
		print('\nBook', key, 'has been added to Catalog.\n')

def get_catalog():
	print(line_break)
	for key in libCatalog:
		print('\n ISBN:', key,'\n',
			'Book Title:', libCatalog[key][0],'\n',
			'Book Author:', libCatalog[key][1],'\n',
			'Book Release Date:', libCatalog[key][2],'\n',
			'Book Genre:', libCatalog[key][3],'\n'
			' Book Quantity:', libCatalog[key][4],'\n')

def search_catalog(libCatalog, value):
	print(line_break)
	print('SEARCH CATALOG')
	fetchCounter = 0

	for key in libCatalog:
		index = 0
		if value == key:
			fetchedResults[key] = [libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3], libCatalog[key][4]]
		else:
			while index < len(libCatalog[key]):
				if value in libCatalog[key][index]:
					fetchedResults[key] = [libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3], libCatalog[key][4]]
					index += 1
				else:
					index += 1

	for key in fetchedResults:
		print('\n Book Number:', key,'\n',
				'Book Title:', fetchedResults[key][0],'\n',
				'Book Author:', fetchedResults[key][1],'\n',
				'Book Release Date:', fetchedResults[key][2],'\n',
				'Book Genre:', fetchedResults[key][3],'\n'
				'Book Quanity:', fetchedResults[key][4],'\n')
		fetchCounter += 1

	return print(fetchCounter, 'Results Found\n', line_break) 

key1001 = add_book('1001', 'Now Read This', 'Nancy Pearl', '2018', 'Kids Fiction', '8')
key1002 = add_book('1002', 'Becoming Fiction', 'Michelle Obama', '2018', 'Autobiography Fiction', '15')
key1003 = add_book('1003', 'To Kill A Mocking Bird', 'Harper Lee', '1960', 'Novel', '4')

def gui():
	initialise = input('\nPress A to add Book: \nPress S to Search Catalog: \nPress V to view Catalog: \nPress Z to cancel: \n\nOption:').upper()

	if initialise == 'A':
		add_to_catalog()
		option = input('Would you like to add an additional book? Y/N\n').upper()
		if option == 'Y':
			add_to_catalog()
		elif option != 'Y':
			gui()


	elif initialise == 'S':
		value = input('Search Catalog: ')
		search_catalog(libCatalog, value)
		gui()

	elif initialise == 'V':
		get_catalog()
		print(len(libCatalog), 'Results Found')
		print(line_break)
		gui()

	elif initialise == 'Z':
		sys.exit(0)

gui()