
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
____________________________________________________

SEARCHING A BOOK

	The Search feature is build to suport a variety of searches, not exclusively IBSN codes. It recursively searches each book to find match. If search value is not an ISBN key, it will search across the columns to find a match. If not match is found, it will continue onto next book, and repeat.

	Any books matched will be temporarily added to a fetchResults dict and will increment a counter, giving total results found. This is what is returned to User. 

	Case sensitive is handled by all existing data and input values being made uppercase.

	Books that have been returned from search, can be borrowed/returned/edited and deleted by selecting specifc book.
____________________________________________________

BORROWING A BOOK

	User can borrow books from either Searching to find book or from view entire catalog. 


		- Search Catalog > Obama > Select Book > Borrow Book > Enter Member ID
		- View Full Catalog > Select Book > Borrow Book > Enter Member ID


	User must have a Member ID before borrowing a book. Non Registered Users will be unable to book book.
	Once ID has been assigned to user, borrowing a book will be available.

	When a member borrows a book, the available quantity for each book will be reduced.

	All borrows and returns rely on member ID. This information is then separatly stored in loanLibrary dictionary.
____________________________________________________

RETURNING A BOOK

	User can return books from either Searching to find book or from view entire catalog. 

		- Search Catalog > Harper Lee > Select Book > Return Book > Enter Member ID
		- View Full Catalog > Select Book > Return Book > Enter Member ID

	User must enter their membership ID in order to return book.

	All borrows and returns rely on member ID. This information is then separatly stored in loanLibrary dictionary.

	Users cannot return a book if no evidence of a borrow can be found in loanLibrary dictionary. User will be asked to check membership ID is correct.
____________________________________________________

ADDING A MEMBER

	Adding a member is necessary to borrow and return any book. This can available in the membership option.
	Member ID's are unique and auto increment from last member added.

		- Membership > Add Member > Enter Full Name

EDITING A MEMBER

	Members Name can be edited by 

		- Membership > View Members > Edit Member

	Members ID is non-editable and is unique for each user.

DELETE A MEMBER
	
	Members can be deleted by 

		- Membership > View Members > Delete Member

	Users will be prompted to confirm deletion.
____________________________________________________

EDITING A BOOK

	All books are editable, besides unique ISBN codes.
	Users can edit Title, Authors, Release Date and Quantity of books.
	Users can edit books through either 

		- Search Catalog > Harper Lee > Select Book > Edit Title etc.
		- View Full Catalog > Select Book > Edit Book > Edit Title etc.

DELETING A BOOK

	All books can be deleted. Books can be deleted by 

		- Search Catalog > Harper Lee > Select Book > Delete Book
		- View Full Catalog > Select Book > Edit Book > Delete Book

Users will be prompted to confirm deletion.

