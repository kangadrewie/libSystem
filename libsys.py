import os
import sys
import requests
import json
from pick import pick

memberID = 1000

libCatalog = dict()
fetchedResults = dict()
loanLibary = dict()
memberLibrary = dict()
line_break = '-' * 40


def add_book(key, bookTitle, bookAuthor, bookReleaseDate, bookQuantity):
	libCatalog[key] = [bookTitle, bookAuthor, bookReleaseDate, bookQuantity]

def add_to_catalog():
	print('ADD BOOK')
	print(line_break)
	isbn_initial = input('Book ISBN: ')
	isbn = isbn_initial.replace('-', '')
	bookQuantity = input('Book Quantity: ')

	api = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:{}&jscmd=data&format=json'.format(isbn))
	data = api.json()
	key = 'ISBN:{}'.format(isbn)

	add_book(key, data[key]['title'], data[key]['authors'][0]['name'], data[key]['publish_date'], bookQuantity)

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
	title = '{:<18s}{:<40s}{:<30s}{:<15s}{}'.format('  ISBN', 'Title', 'Author', 'Release Date', 'Quantity')

	options = ['[GO BACK TO MENU]']

	for key in libCatalog:
		string = '{:<16s}{:<40s}{:<30s}{:<15s}{:<5d}'.format(key[5:], libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3])
		options.append(string)
	option, initialise = pick(options, title)

	if initialise == 0:
		menu()
	elif initialise >=1:
		title = 'What would like to do?'
		options = ['Borrow Book', 'Return Book']
		option, initialise = pick(options, title)

		if initialise == 0:
			borrowBook(initialise)
		elif initialise == 1:
			returnBook(initialise)

		# loanLibary.append(loanDetails)


def search_catalog(libCatalog, value):

	fetchCounter = 0

	for key in libCatalog:
		index = 0
		if value == key:
			fetchedResults[key] = [libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3]]
		else:
			while index < len(libCatalog[key]) - 1:
				if value in libCatalog[key][index]:
					fetchedResults[key] = [libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3]]
					index += 1
				else:
					index += 1

	title = '{:<18s}{:<40s}{:<30s}{:<15s}{}'.format('  ISBN', 'Title', 'Author', 'Release Date', 'Quantity')

	options = ['[GO BACK TO MENU]']

	for key in fetchedResults:
		string = '{:<16s}{:<40s}{:<30s}{:<15s}{:<5d}'.format(key[5:], fetchedResults[key][0], fetchedResults[key][1], fetchedResults[key][2], fetchedResults[key][3])
		options.append(string)
		fetchCounter += 1
	options.append('{} Results Found'.format(fetchCounter))
	option, initialise = pick(options, title)
	print(len(options))
	if initialise == 0 or initialise == len(options) - 1:
		menu()
		

def borrowBook(initialise):
	memberID = int(input('Enter Member ID:'))
	memberName = ''
	bookISBN = list(libCatalog)[initialise+1]
	bookTitle = libCatalog[bookISBN][0]

	for memberID in memberLibrary:
		memberID = memberID
		memberName = memberLibrary[memberID][0]

	loanDetails = '{}{}{}{}'.format(memberID, memberName, bookISBN, bookTitle)
	reduceQuantity = int(libCatalog[bookISBN][-1]) - 1
	libCatalog[bookISBN][-1] = reduceQuantity
	loanLibary[memberID] = [memberName, bookISBN, bookTitle]
	menu()

def returnBook(initialise):
	memberID = int(input('Enter Member ID:'))
	bookISBN = list(libCatalog)[initialise]
	print(bookISBN)
	increaseQuantity = int(libCatalog[bookISBN][-1]) + 1
	libCatalog[bookISBN][-1] = increaseQuantity
	loanLibary.pop(memberID, None)
	menu()


def addMember():
	print('Add Member')
	print(line_break)
	memberID = 1000
	for i in memberLibrary:
		memberID = i + 1

	print('Membership ID', memberID)

	name = input('Member Name:')
	memberLibrary[memberID] = [name]

	title = '\nMember {} has been added to Catalog.\n\nWould you like to add an additional Member?'.format(name)
	options = ['Yes', 'No']
	option, initialise = pick(options, title)

	if initialise == 0:
		os.system('clear')
		addMember()
	elif initialise == 1:
		menu()

def getMember():
	title = '{:<18s}{:<42s}'.format('  Member ID', 'Name')
	options = ['[GO BACK TO MENU]']
	for key in memberLibrary:
		string = '{:<16d}{:<40s}'.format(key, memberLibrary[key][0])
		options.append(string)

	option, initialise = pick(options, title)
	print(len(options))
	if initialise == 0:
		menu()

key1001 = add_book('ISBN:9780980200447', 'Now Read This', 'Nancy Pearl', '2018', 8)
key1002 = add_book('ISBN:9780980200448', 'Becoming Fiction', 'Michelle Obama', '2018', 15)
key1003 = add_book('ISBN:9780980200449', 'To Kill A Mocking Bird', 'Harper Lee', '1960', 4)

def menu():
	os.system('clear')
	title = 'Library System 1.0'
	options = ['Add Book', 'Search Catalog', 'Membership', 'View Catalog', 'Exit']
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

	elif initialise == 2:

		title = 'Membership'
		options = ['View Members', 'Add Member', 'Go Back']
		option, initialise = pick(options, title)

		if initialise == 0:
			getMember()
		elif initialise == 1:
			addMember()
		elif initialise == 2:
			menu()

	elif initialise == 3:
		get_catalog()
		print(line_break)
		escape_input = input().upper()

	elif initialise == 4:
		sys.exit(0)

menu()