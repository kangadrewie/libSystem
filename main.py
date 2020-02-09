libCatalog = dict()
fetchResults = dict()


class AddBook():
	# Class constructor
	def __init__(self, key, bookTitle, bookAuthor, bookReleaseDate, bookGenre):
		self.key = key
		self.bookTitle = bookTitle
		self.bookAuthor = bookAuthor
		self.bookReleaseDate = bookReleaseDate
		self.bookGenre = bookGenre

	# Adds book to Catalog
	def addBook(self):
		libCatalog[self.key] = [self.bookTitle, self.bookAuthor, self.bookReleaseDate, self.bookGenre]



def searchBook(libCatalog, value):
	fetchCounter = 0

	for key in libCatalog:
		index = 0
		if value in key:
			fetchResults[key] = [libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3]]
		else:
			while index < 4:
				if value in libCatalog[key][index]:
					fetchResults[key] = [libCatalog[key][0], libCatalog[key][1], libCatalog[key][2], libCatalog[key][3]]
					index += 1
				else:
					index += 1

	# Error Checking
	
	for key in fetchResults:
		print(' Book Number:', key,'\n',
				'Book Title:', fetchResults[key][0],'\n',
				'Book Author:', fetchResults[key][1],'\n',
				'Book Release Date:', fetchResults[key][2],'\n',
				'Book Genre:', fetchResults[key][3],'\n')
		fetchCounter += 1

	return print(fetchCounter, 'Results Found')

			# print(' Book Number:', key,'\n',
			# 	'Book Title:', libCatalog[key][0],'\n',
			# 	'Book Author:', libCatalog[key][1],'\n',
			# 	'Book Release Date:', libCatalog[key][2],'\n',
			# 	'Book Genre:', libCatalog[key][3],'\n')

# WHAT DO YOU WANT TO DO
# ADD
# FIND


key1001 = AddBook('1001', 'Now Read This', 'Nancy Pearl', '2018', 'Kids Fiction')
key1002 = AddBook('1002', 'Becoming Fiction', 'Michelle Obama', '2018', 'Autobiography Fiction')
key1003 = AddBook('1003', 'To Kill A Mocking Bird', 'Harper Lee', '1960', 'Novel')
key1001.addBook()
key1002.addBook()
key1003.addBook()

# print(libCatalog)

char = str(input('Search Catalog: '))
searchBook(libCatalog, char)