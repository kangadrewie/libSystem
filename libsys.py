import os
import sys
import requests
import json
from pick import pick

libCatalog = dict()
fetchedResults = dict()
loanLibary = dict()
line_break = '-------------------------------------------'

def add_book(key, bookTitle, bookAuthor, bookReleaseDate, bookPublisher, bookQuantity):
	libCatalog[key] = [bookTitle, bookAuthor, bookReleaseDate, bookPublisher, bookQuantity]

def add_to_catalog():
	print(line_break)
	print('ADD BOOK\n')
	isbn = input('Book ISBN: ')
	bookQuantity = input('Book Quantity: ')

	api = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:{}&jscmd=data&format=json'.format(isbn))
	data = api.json()
	key = 'ISBN:{}'.format(isbn)

	add_book(key, data[key]['title'], data[key]['authors'][0]['name'], data[key]['publish_date'], data[key]['publishers'][0]['name'], bookQuantity)

	title = '\nBook {} has been added to Catalog.\n\nWould you like to add an additional book?'.format(key[5:])
	options = ['Yes', 'No']
	option, initialise = pick(options, title)

	if initialise == 0:
		os.system('clear')
		add_to_catalog()
	elif initialise == 1:
		menu()


def get_catalog():
	print(line_break)
	title = ''
	options = ['Title:{}:{}Release Date:{}Publisher:Quantity:', '\n\n\n\n\n\n\nHELLO']
	# for key in libCatalog:
	# 	string = '{}\nTitle:{}\nAuthor:{}\nRelease Date:{}\nPublisher:\nQuantity:{}'.format(key, libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3], libCatalog[key][4])
	# 	print(string)
		# options.append(string)
	# print(options)
	option, initialise = pick(options, title)

	# for key in libCatalog:
	# 	print('\n', key,'\n',
	# 		'Title:', libCatalog[key][0],'\n',
	# 		'Author:', libCatalog[key][1],'\n',
	# 		'Release Date:', libCatalog[key][2],'\n',
	# 		'Publisher:', libCatalog[key][3],'\n'
	# 		' Quantity:', libCatalog[key][4],'\n')

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
		print('\n', key,'\n',
				'Title:', fetchedResults[key][0],'\n',
				'Author:', fetchedResults[key][1],'\n',
				'Release Date:', fetchedResults[key][2],'\n',
				'Publisher:', fetchedResults[key][3],'\n'
				' Quanity:', fetchedResults[key][4],'\n')
		fetchCounter += 1
		

	return print(fetchCounter, 'Results Found\n', line_break)

def borrowReturn(libCatalog, value):
	search_catalog(libCatalog, value)

key1001 = add_book('1001', 'Now Read This', 'Nancy Pearl', '2018', 'Litwin Books ', '8')
key1002 = add_book('1002', 'Becoming Fiction', 'Michelle Obama', '2018', 'Litwin Books ', '15')
key1003 = add_book('1003', 'To Kill A Mocking Bird', 'Harper Lee', '1960', 'Litwin Books ', '4')

def menu():
	os.system('clear')
	title = ''
	options = ['Add Book', 'Search Catalog', 'Borrow Book', 'View Catalog', 'Cancel']
	option, initialise = pick(options, title)
	gui(initialise)


def gui(initialise):
	# initialise = input('\nPress A to add Book: \nPress S to Search Catalog: \nPress B to Borrow Book: \nPress V to view Catalog: \nPress Z to cancel: \n\nOption:').upper()

	if initialise == 0:
		add_to_catalog()

	elif initialise == 1:
		value = input('Search Catalog: ')
		search_catalog(libCatalog, value)
		print('Press M to go back to menu')
		escape_input = input().upper()
		if escape_input == 'M':
			menu()

	elif initialise == 3:
		get_catalog()
		print(len(libCatalog), 'Results Found')
		print(line_break)
		print('Press M to go back to menu')
		escape_input = input().upper()
		if escape_input == 'M':
			menu()

	elif initialise == 4:
		sys.exit(0)

menu()