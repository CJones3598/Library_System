# Import SQLite3 module and Error class for database functionality
import sqlite3
from sqlite3 import Error

# Functions for input validations
def get_valid_input(prompt):
    while True:
        # Get user input, remove leading/trailing whitespaces, and convert to uppercase
        user_input = input(prompt).strip().upper()
        # Check if the input is non-empty
        if user_input:
            # Return the valid input and exit the loop
            return user_input
        else:
            # Print a message for the user to enter a valid input and continue the loop
            print("Please enter a valid input.")
def get_integer_input(prompt):
    while True:
        try:
            # Check if user input is an integer, if integer return value
            user_input = int(input(prompt))
            return user_input
        # If value not integer, return an error and prompt input
        except ValueError:
            print("Invalid input. Please enter a valid option")

# Function to connect to SQLite3 database
def database_connection():
    # Creates connection with SQLite3 database and creates cursor object
    connect = sqlite3.connect('library.db')
    cursor = connect.cursor()
    return connect, cursor
# Function to create tables in SQLite3 database
def create_tables():
    try:
        # Connect to library DB and create a cursor
        connect, cursor = database_connection()
       # Create a table to store book information 
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            isbn TEXT,
            pub_date TEXT,
            genre TEXT,
            quantity INTEGER
        )
    ''')
    # Handles SQLite3 errors, displays error to user
    except Error as e:
        print("Error occurred -", e)
    # Commits changes and closes connection, displays connection status to user
    finally:
        if connect:
            connect.commit()
            connect.close()
            print("Connection with database established.")

# Function to display staff main menu
def staff_main_menu():
   # Print Application Name and staff options to users for input
   print('''Library Management System\n
            Welcome to the library management system.\n
            1. View All Books
            2. Add New Book
            3. Delete Book
            4. Update Book Quantity
            5. Update Book Information
            6. Check Book Stock Status
            0. Exit
         ''')
   
# Function to view all books in library - staff function 
def view_all_books():
    # Creates connection with SQLite3 database and creates cursor object
    connect, cursor = database_connection()
    # Execute a SELECT query to retrieve columns and data from the books table
    cursor.execute('''
        SELECT book_id, title, author, isbn, pub_date, genre, quantity
        FROM books
    ''')
    # Fetch all results obtained from SELECT query
    books = cursor.fetchall()
    # Close SQLite3 database connection
    connect.close()
    # Check if there are any books in the books table
    if books:
        # If there are books, print a header for the book information to the user
        print("All Books in the Library:")
        # Print a formatted header with column names to the user
        print("{:<5} {:<25} {:20} {:<15} {:<12} {:<30} {:<8}".format("ID", "Title", "Author", "ISBN", "Date", "Genre", "Quantity"))
        for book in books:
            # Print formatted information for each book in books table
            print("{:<5} {:<25} {:<20} {:<15} {:<12} {:<30} {:<8}".format(*book))
    else:
        # Error handling if no data in books table
        print("No books found in the library.")

# Function to add book to library - staff function
def add_book():
    # Creates connection with SQLite3 database and creates cursor object
    connect, cursor = database_connection()
    # User input fields for adding new book to table
    title = get_valid_input("Please Enter Book Title: ")
    author = get_valid_input("Please Enter Book Author: ")
    isbn = get_valid_input("Please Enter Book ISBN: ")
    pub_date = get_valid_input("Please Enter Book Publication Date (YYYY-MM-DD): ")
    genre = get_valid_input("Please Enter Book Genre: ")
    quantity = get_integer_input("Please Enter Book Quantity: ")
    # Queries to insert new record into books table in database
    cursor.execute('''
        INSERT INTO books (title, author, isbn, pub_date, genre, quantity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, author, isbn, pub_date, genre, quantity))
    # Display data inserted into table to user
    print("Data inserted into table: ")
    last_added = cursor.execute('''SELECT * FROM books ORDER BY book_id DESC LIMIT 1''').fetchone()
    print("{:<5} {:<25} {:20} {:<15} {:<12} {:<30} {:<8}".format("ID", "Title", "Author", "ISBN", "Date", "Genre", "Quantity"))
    print("{:<5} {:<25} {:<20} {:<15} {:<12} {:<30} {:<8}".format(*last_added))
    # Commit table and database changes and close connection
    connect.commit()
    connect.close()

# Function to remove book from library - staff function
def remove_book():
    # Creates connection with SQLite3 database and creates cursor object
    connect, cursor = database_connection()
    book_id = get_integer_input("Please Enter Book ID: ")
    # Check if the book with the specified ID exists
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    result = cursor.fetchone()
    if result:
        # Book found, proceed with deletion, commit changes and print deletion confirmation to the user
        cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
        connect.commit()
        print("Book removed from the database")
    else:
        # Error handling for book not found in table
        print(f"No book found with ID: {book_id}")

# Function to update quantity of a book - staff function
def update_book_quantity():
     # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User input for book id
    book_id = get_integer_input("Please Enter the Book ID: ")
    # Fetch the current book name and quantity before updating
    cursor.execute('''
        SELECT title, quantity
        FROM books
        WHERE book_id = ?
    ''', (book_id,))
    # Fetch Result from SELECT query to check if book id exists in table
    result = cursor.fetchone()
    if result:
        # User input for new book quantity
        new_quantity = get_integer_input("Please Enter New Quantity: ")
        # Update the quantity of the specified book
        cursor.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))
        print(f"Quantity for {result[0]} updated to: {new_quantity}.")
    else:
        # Error handling for book not found in table
        print(f"No book found with ID: {book_id}")
    # Commit changes and close the database connection
    connect.commit()
    connect.close()

# Function to update book information - staff function
def update_book_information():
     # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    book_id = get_integer_input("Please Enter Book ID: ")
    # Check if book exists in table and fetch result
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    result = cursor.fetchone()
    # If book exists, prompt user input for new book information
    if result:
        new_title = get_valid_input("Please Enter New Title: ")
        new_author = get_valid_input("Please Enter New Author: ")
        new_isbn = get_valid_input("Please Enter New ISBN: ")
        new_pub_date = get_valid_input("Please Enter New Publication Date(YYYY-MM-DD): ")
        new_genre = get_valid_input("Please Enter New Genre: ")
        # Execute an SQL UPDATE statement to modify the quantity of the specified item
        cursor.execute('''
            UPDATE books
            SET title = ?, author = ?, isbn = ?, pub_date = ?, genre = ?
            WHERE book_id = ?
            ''', (new_title, new_author, new_isbn, new_pub_date, new_genre, book_id))
        print(f"Information for {result[1]} updated.")
    else:
        # Error handling for book not found in table
        print(f"No book found with ID: {book_id}")
    # Commit changes to database and close database connection
    connect.commit()
    connect.close()

# Function to check book stock status - staff function
def check_book_status():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    book_id = get_integer_input("Please Enter Book ID: ")
    # Execute an SQL SELECT statement to retrieve the quantity of the specified item
    cursor.execute('''
        SELECT title, quantity
        FROM books
        WHERE book_id = ?
    ''', (book_id,))
    # Fetch the result of the SELECT query
    result = cursor.fetchone()
    # Close the database connection
    connect.close()
    # Check if a result is found
    if result:
        # Check the quantity and display the stock status
        if result[1] >= 1:
            print(f"Book: {result[0]} is In stock with {result[1]} units")
        else:
            print(f"Book: {result[0]} is Out of stock")
    else:
        # Error handling for book not found in table
        print(f"Book not found with ID: {book_id}")

if __name__ == "__main__":
    # Create tables in database if they do not exist
    create_tables()
    while True:
        # Displays staff main menu and prompts user choice input
        staff_main_menu()
        choice = input("Enter your choice 0-5: ")

        if choice == "0":
            # Exit Program
            print("Exiting Program. Goodbye!")
            break
        elif choice == "1":
            # View all books in library
            view_all_books()
        elif choice == "2":
            # Add a new book to the library
            add_book()
        elif choice == "3":
            # Remove a book from the library
            remove_book()
        elif choice == "4":
            # Update the quantity of a book in the library
            update_book_quantity()
        elif choice == "5":
            # Update the information of a book in the library
            update_book_information()
        elif choice == "6":
            # Check the stock status of a book in the library
            check_book_status()
