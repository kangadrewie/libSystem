import os
import sys
import requests
import json
from pick import pick

memberID = 1000
selectedBook = 0

libCatalog = dict()
fetchedResults = dict()
loanLibary = dict()
memberLibrary = dict()
line_break = '-' * 40

'''
HOW TO USE

	Libsys.py is a shell script that can be run in terminal or IDE. It's functionality ranges from
		- Automatic ISBN Search retrieval using Open Library's RESTful API
		- Manual Book Import
		- Add/Edit/Delete Books
		- Add/Edit/Delete Members
		- Recursive Search Feature
		- All Users can Borrow and Return Book

	Prior to using, users must install pick by pip install pick.
	Pick a lightweight library that is used to help create curses based interactive selection list in the terminal.
	Documentation can be found here - https://pypi.org/project/pick/
____________________________________________________

ADDING A BOOK

	Users have two options to add a book.

		- First is manually entering the books details incl. ISBN, Title, Author, Release Date, and Quantity, by Add Book > Manually Add Book. This is then stored in a libCatalog dict.

		- Alternatively, users can Add Book > Automatic ISBN Search which will search Open Librarys RESTful API and return the above information.

		Data is returned in JSON format, then parse and stored in library catalog dictionary.

		Exceptions are configured to catch any ISBN that returns no data. Or is simply invalid ie. KeyError, ValueError.
____________________________________________________'''

def add_book(key, bookTitle, bookAuthor, bookReleaseDate, bookQuantity):
	libCatalog[key] = [bookTitle.upper(), bookAuthor.upper(), bookReleaseDate.upper(), bookQuantity]

# Manual Add Function
def manualAddBook():
	os.system('clear')
	for i in range(1):
		key = input('Book ISBN: ')
		bookTitle = input('Book Title: ')
		bookAuthor = input('Book Author: ')
		bookReleaseDate = input('Book Release Date: ')
		bookQuantity = int(input('Book Quantity: '))
	add_book(key, bookTitle, bookAuthor, bookReleaseDate, bookQuantity)
	menu()

'''
API Handling
'''
def add_to_catalog():
	title = 'ADD BOOK'
	options = ['Automatic ISBN Search', 'Enter Book Details Manually', 'Return to Menu']

	option, initialise = pick(options, title)

	try:
		if initialise == 0:
			isbn_initial = input('Book ISBN: ')
			isbn = isbn_initial.replace('-', '')
			bookQuantity = int(input('Book Quantity: '))

			api = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:{}&jscmd=data&format=json'.format(isbn))
			data = api.json()
			key = 'ISBN:{}'.format(isbn)
			print(api.status_code)
			if api.status_code == 200 and len(data) >= 1:
				add_book(key, data[key]['title'], data[key]['authors'][0]['name'], data[key]['publish_date'], bookQuantity)

				title = '\nBook {} has been added to Catalog.\n\nWould you like to add an additional book?'.format(key[5:])
				options = ['Yes', 'No']
				option, initialise = pick(options, title)

				if initialise == 0:
					os.system('clear')
					add_to_catalog()
				elif initialise == 1:
					menu()
			else:
				title = 'Invalid ISBN Code. Please try again'
				options = ['Enter Book Details Manually', 'Return to Menu']
				option, initialise = pick(options, title)
				
				if initialise == 0:
					manualAddBook()

				elif initialise == 1:
					menu()
		elif initialise == 1:
			manualAddBook()
		elif initialise == 2:
			menu()
	except KeyError:
		title = 'Unable to import book.'
		options = ['Enter Book Details Manually', 'Return to Menu']
		option, initialise = pick(options, title)
		
		if initialise == 0:
			manualAddBook()

		elif initialise == 1:
			menu()
	except ValueError:
		title = 'Invalid Entry. Please ensure input is valid.'
		options = ['Return to Menu']
		option, initialise = pick(options, title)
		
		if initialise == 0:
			menu()	

'''
Function to retrieve all booked currently stored on system to User Interface. 

Books are formatted and sent to pick function for curses gui option. 
User can use arrow keys or mouse wheel to select books and options.
'''
def get_catalog():
	print(line_break)
	title = '{:<18s}{:<40s}{:<30s}{:<15s}{}'.format('  ISBN', 'Title', 'Author', 'Release Date', 'Quantity')

	options = ['[GO BACK TO MENU]']

	for key in libCatalog:
		string = '{:<16s}{:<40s}{:<30s}{:<15s}{:<5d}'.format(key[5:], libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3])
		options.append(string)
	option, selectedBook = pick(options, title)

	if selectedBook == 0:
		menu()
	elif selectedBook >=1:
		title = 'What would like to do?'
		options = ['Edit Book', 'Borrow Book', 'Return Book', 'Delete Book', 'Return to Menu']
		option, initialise = pick(options, title)

		if initialise == 1:
			borrowBook(libCatalog, selectedBook)
		elif initialise == 2:
			returnBook(libCatalog, selectedBook)
		elif initialise == 0:
			editBook(libCatalog, selectedBook)
		elif initialise == 3:
			deleteBook(libCatalog, selectedBook)
		elif initialise == 4:
			menu()


"""
SEARCHING A BOOK

	The Search feature is build to suport a variety of searches, not exclusively IBSN codes. It recursively searches each book to find match. If search value is not an ISBN key, it will search across the columns to find a match. If not match is found, it will continue onto next book, and repeat.

	Any books matched will be temporarily added to a fetchResults dict and will increment a counter, giving total results found. This is what is returned to User. 

	Case sensitive is handled by all existing data and input values being made uppercase.

	Books that have been returned from search, can be borrowed/returned/edited and deleted by selecting specifc book.
____________________________________________________"""

def search_catalog(libCatalog, value):

	fetchCounter = 0
	fetchedResults = dict()
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
	option, selectedBook = pick(options, title)

	if selectedBook == 0 or selectedBook == len(options) - 1:
		menu()
	elif selectedBook >=1:
		title = 'What would like to do?'
		options = ['Edit Book', 'Borrow Book', 'Return Book', 'Delete Book', 'Return to Menu']
		option, initialise = pick(options, title)

		if initialise == 1:
			borrowBook(fetchedResults, selectedBook)
		elif initialise == 2:
			returnBook(fetchedResults, selectedBook)
		elif initialise == 0:
			editBook(fetchedResults, selectedBook)
		elif initialise == 3:
			deleteBook(fetchedResults, selectedBook)
		elif initialise == 4:
			menu()
		
'''
BORROWING A BOOK

	User can borrow books from either Searching to find book or from view entire catalog. 


		- Search Catalog > Obama > Select Book > Borrow Book > Enter Member ID
		- View Full Catalog > Select Book > Borrow Book > Enter Member ID


	User must have a Member ID before borrowing a book. Non Registered Users will be unable to book book.
	Once ID has been assigned to user, borrowing a book will be available.

	When a member borrows a book, the available quantity for each book will be reduced.

	All borrows and returns rely on member ID. This information is then separatly stored in loanLibrary dictionary.
____________________________________________________'''

def borrowBook(catalog, initialise):
	memberID = int(input('Enter Member ID:'))
	memberName = ''
	bookISBN = list(catalog)[initialise-1]
	bookTitle = catalog[bookISBN][0]

	if memberID not in memberLibrary:
		title = 'Member {} does not exist. Please add member before loaning book.'.format(memberID)
		options = ['GO BACK TO MENU']
		option, initialise = pick(options, title)
		if initialise == 0:
			menu()
	else:
		memberID = memberID
		memberName = memberLibrary[memberID][0]

		loanDetails = '{}{}{}{}'.format(memberID, memberName, bookISBN, bookTitle)

		for bookISBN in libCatalog:
			reduceQuantity = int(libCatalog[bookISBN][-1]) - 1
			libCatalog[bookISBN][-1] = reduceQuantity

		loanLibary[memberID] = [memberName, bookISBN, bookTitle]

		title = 'Member {} has successfully loaned {}.'.format(memberID, bookTitle)
		options = ['GO BACK TO MENU']
		option, initialise = pick(options, title)
		if initialise == 0:
			menu()

'''
RETURNING A BOOK

	User can return books from either Searching to find book or from view entire catalog. 

		- Search Catalog > Harper Lee > Select Book > Return Book > Enter Member ID
		- View Full Catalog > Select Book > Return Book > Enter Member ID

	User must enter their membership ID in order to return book.

	All borrows and returns rely on member ID. This information is then separatly stored in loanLibrary dictionary.

	Users cannot return a book if no evidence of a borrow can be found in loanLibrary dictionary. User will be asked to check membership ID is correct.
____________________________________________________'''

def returnBook(catalog, initialise):
	memberID = int(input('Enter Member ID:'))
	bookISBN = list(catalog)[initialise-1]

	if memberID not in loanLibary:
		title = 'Member {} has not loan this book. Please check Member ID.'.format(memberID)
		options = ['GO BACK TO MENU']
		option, initialise = pick(options, title)
		if initialise == 0:
			menu()
	else:
		for bookISBN in libCatalog:
			increaseQuantity = int(libCatalog[bookISBN][-1]) + 1
			libCatalog[bookISBN][-1] = increaseQuantity
			loanLibary.pop(memberID, None)

		title = 'Book has been successfully returned.'
		options = ['GO BACK TO MENU']
		option, initialise = pick(options, title)
		if initialise == 0:
			menu()

'''
ADDING A MEMBER

	Adding a member is necessary to borrow and return any book. This can available in the membership option.
	Member ID's are unique and auto increment from last member added.

		- Membership > Add Member > Enter Full Name
'''
def addMember():
	print('Add Member')
	print(line_break)
	memberID = 1000
	for i in memberLibrary:
		memberID = i + 1

	print('Membership ID', memberID)

	name = input('Member Name:').upper()
	memberLibrary[memberID] = [name]

	title = '\nMember {} has been added to Catalog.\n\nWould you like to add an additional Member?'.format(name)
	options = ['Yes', 'No']
	option, initialise = pick(options, title)

	if initialise == 0:
		os.system('clear')
		addMember()
	elif initialise == 1:
		menu()

'''
All current registered members can be view from Membership > View Members
'''
def getMember():
	title = '{:<18s}{:<42s}'.format('  Member ID', 'Name')
	options = ['[GO BACK TO MENU]']
	for key in memberLibrary:
		string = '{:<16d}{:<40s}'.format(key, memberLibrary[key][0])
		options.append(string)

	option, selectedMember = pick(options, title)
	if selectedMember == 0:
		menu()
	elif selectedMember >=1:
			title = 'What would like to do?'
			options = ['Edit Member', 'Delete Member', 'Return to Menu']
			option, initialise = pick(options, title)

			if initialise == 0:
				editMember(selectedMember)
			elif initialise == 1:
				deleteMember(selectedMember)
			elif initialise == 2:
				menu()
'''
EDITING A MEMBER

	Members Name can be edited by 

		- Membership > View Members > Edit Member

	Members ID is non-editable and is unique for each user.
'''
def editMember(initialise):
	memberID = list(memberLibrary)[initialise-1]
	editName = input('Edit Name:')
	memberLibrary[memberID][0] = editName.upper()
	menu()

'''
DELETE A MEMBER
	
	Members can be deleted by 

		- Membership > View Members > Delete Member

	Users will be prompted to confirm deletion.
'''
def deleteMember(initialise):
	memberID = list(memberLibrary)[initialise-1]
	title = 'Are you sure you want to delete Member {}'.format(memberID)
	options = ['Yes', 'No']

	option, initialise = pick(options, title)

	if initialise == 0:
		memberLibrary.pop(memberID, None)
		menu()
	else:
		menu()
'''
EDITING A BOOK

	All books are editable, besides unique ISBN codes.
	Users can edit Title, Authors, Release Date and Quantity of books.
	Users can edit books through either 

		- Search Catalog > Harper Lee > Select Book > Edit Title etc.
		- View Full Catalog > Select Book > Edit Book > Edit Title etc.
'''
def editBook(catalog, initialise):
	bookISBN = list(catalog)[initialise-1]
	title = 'ISBN Codes are non-editable.'
	options = ['Edit Title', 'Edit Author', 'Edit Release Date', 'Edit Quantity', 'Return to Menu']

	option, initialise = pick(options, title)

	try:
		if initialise == 0:
			newTitle = input('Enter Title:')
			libCatalog[bookISBN][0] = newTitle.upper()
			menu()
		elif initialise == 1:
			newAuthor = input('Enter Author(s):')
			libCatalog[bookISBN][1] = newAuthor.upper()
			menu()
		elif initialise == 2:
			newReleaseDate = input('Enter Release Date:')
			libCatalog[bookISBN][2] = newReleaseDate.upper()
			menu()
		elif initialise == 3:
			newQuantity = int(input('Enter Quantity:'))
			libCatalog[bookISBN][3] = newQuantity
			menu()
		elif initialise == 4:
			menu()
	except ValueError:
		title = 'Invalid Entry. Please ensure Quantity is an valid integer.'
		options = ['Return to Menu']
		option, initialise = pick(options, title)
		
		if initialise == 0:
			menu()		
'''
DELETING A BOOK

	All books can be deleted. Books can be deleted by 

		- Search Catalog > Harper Lee > Select Book > Delete Book
		- View Full Catalog > Select Book > Edit Book > Delete Book

Users will be prompted to confirm deletion.
'''
def deleteBook(catalog, initialise):
	bookISBN = list(catalog)[initialise-1]
	title = 'Are you sure you want to delete book {}'.format(bookISBN)
	options = ['Yes', 'No']

	option, initialise = pick(options, title)

	if initialise == 0:
		libCatalog.pop(bookISBN, None)
		menu()
	else:
		menu()

'''
Some hardcoded books for demonstration purposes.
'''
key1001 = add_book('ISBN:9780980200447', 'Now Read This', 'Nancy Pearl', '2018', 8)
key1002 = add_book('ISBN:9780980200448', 'Becoming', 'Michelle Obama', '2018', 15)
key1003 = add_book('ISBN:9780980200449', 'To Kill A Mocking Bird', 'Harper Lee', '1960', 4)
key1004 = add_book('ISBN:9780980200450', 'Educated: A Memoir', 'Tara Westover', '2019', 9)
key1005 = add_book('ISBN:9780980200451', 'Where the Crawdads Sing', 'Delia Owens', '2020', 11)

'''
GUI and Menu Handling.
'''
def menu():
	os.system('clear')
	title = 'Library System 1.0 by Andrew Gorman'
	options = ['Add Book', 'Search Catalog', 'Borrows and Returns', 'Memberships', 'View Full Catalog', 'Exit']
	option, initialise = pick(options, title)
	gui(initialise)


def gui(initialise):

	if initialise == 0:
		os.system('clear')
		add_to_catalog()

	elif initialise == 1:
		os.system('clear')
		value = input('Search Catalog: ').upper()
		search_catalog(libCatalog, value)

	elif initialise == 2:
		os.system('clear')
		value = input('Find Book to Borrow/Return:').upper()
		search_catalog(libCatalog, value)

	elif initialise == 3:
		os.system('clear')
		title = 'Membership'
		options = ['View Members', 'Add Member', 'Return to Menu']
		option, initialise = pick(options, title)

		if initialise == 0:
			getMember()
		elif initialise == 1:
			addMember()
		elif initialise == 2:
			menu()

	elif initialise == 4:
		os.system('clear')
		get_catalog()

	elif initialise == 5:
		sys.exit(0)

menu()