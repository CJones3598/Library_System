# Import SQLite3 module and Error class for database functionality
import sqlite3
from sqlite3 import Error
# Import hashlib module for password hashing
import hashlib
# Import random module for username creation
import random
# Import datetime and timedelta class from datetime module for transactions
from datetime import datetime, timedelta

# Global variables for username of user logged in
current_user = None

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
def get_access_input(prompt):
    while True:
        try:
            # Check if user input is an integer
            user_input = int(input(prompt))

            # Check if the input is either 1 or 5
            if user_input in [1, 5]:
                return user_input
            else:
                print("Invalid input. Please enter either 1 or 5.")
        except ValueError:
            print("Invalid input. Please enter a valid input.")

# Functions to connect to SQLite3 database and create tables in database
def database_connection():
    # Creates connection with SQLite3 database and creates cursor object
    connect = sqlite3.connect('library.db')
    cursor = connect.cursor()
    connect.execute("PRAGMA foreign_keys = 1")
    return connect, cursor
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
        # Create a table to store staff information 
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff_information (
            staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            job_role TEXT
        )
    ''')
        # Create a table to store staff user accounts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff_accounts (
            username TEXT PRIMARY KEY,
            password TEXT,
            access_level INTEGER,
            staff_id INTEGER,
            FOREIGN KEY (staff_id) REFERENCES staff_information (staff_id)
        )
    ''')
                 # Create a table to store customer information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_information (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        )
    ''')
        # Create a table to store customer accounts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_accounts (
            username TEXT PRIMARY KEY,
            password TEXT,
            customer_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customer_information (customer_id)
        )
    ''')
       # Create a table to store book information 
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            book_id INTEGER,
            borrow_date TEXT,
            return_date TEXT,
            date_returned TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer_information (customer_id),
            FOREIGN KEY (book_id) REFERENCES books (book_id)
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
def main_menu():
    print('''Library Management System\n
                    Welcome to the library management system.\n
                    1. Staff Portal
                    2. Customer Portal
                    0. Exit
                ''')

# Functions for username generation and password hashing  
def generate_username(first_name, last_name, account_type):
    connection, cursor = database_connection()
    while True:
        # Generate a username using uppercase first name, last name, and 2 random numbers
        username = f"{first_name.upper()}.{last_name.upper()}{random.randint(0, 9)}{random.randint(0, 9)}"
        # Check if the username already exists in staff_accounts table
        cursor.execute(f'''
            SELECT COUNT(*) FROM {account_type} WHERE username = ?
        ''', (username,))
        count = cursor.fetchone()[0]
        # If the count is 0, the username is unique
        if count == 0:
            return username
def hash_password(password):
    # Use hashlib to hash user input password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# Function for login system
def login(account_type):
    # Fetch global variable for the username of current logged in user
    global current_user
    # Creates connection with SQLite3 database and creates cursor object
    connect, cursor = database_connection()
    # Create a variable for login attempts
    attempts = 0
    # Login block for more than 5 invalid logins
    while attempts < 5:
        # Take user input for username and password
        username = get_valid_input("Enter username: ")
        password = get_valid_input("Enter password: ")
        # Hash the password for comparison
        hashed_password = hash_password(password)
        # Check if the username and hashed password match in staff_accounts table
        cursor.execute(f'SELECT * FROM {account_type} WHERE username=? AND password=?', (username, hashed_password))
        # Fetch the result from the SELECT query
        account = cursor.fetchone()
        # If the account is valid proceed with login
        if account:
            print("Login successful.")
            # You can add further logic for staff login success
            if account_type == "staff_accounts":
                current_user = username
                staff_main_menu()
                break  # Exit the loop after staff_main_menu() execution
            elif account_type  == "customer_accounts":
                current_user = username
                customer_main_menu()
            # Error Handling if the account is not valid
            else:
                print("Invalid Account")
        else:
            # Login Block calculations for attempts
            attempts += 1
            remaining_attempts = 5 - attempts
            print(f"Invalid username or password. Remaining attempts: {remaining_attempts}")
    # Maximum Login attempt handling
    print("Exceeded maximum login attempts. Closing the program.")
    exit()

# Functions for user account management
def create_admin():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # Set variable for admin account
    username = 'ADMIN'
    password = 'ADMIN'
    hashed_password = hash_password(password)
    # Check if admin user exists
    cursor.execute('SELECT * FROM staff_accounts WHERE username=?', (username,))
    admin_exists = cursor.fetchone()
    # If admin account doesnt exist, create one
    if not admin_exists:
        cursor.execute('INSERT INTO staff_accounts VALUES (?, ?, ?, ?)', (username, hashed_password, "5", "0"))
        print("Administrator account created with username 'ADMIN' and password 'ADMIN'\nPlease change the password after login.")
        # Commit the changes and close the connection to SQLite database
        connect.commit()
        connect.close()
def staff_register():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User inputs for staff information
    first_name = get_valid_input("Enter first name: ")
    last_name = get_valid_input("Enter last name: ")
    job_role = get_valid_input("Enter job role: ")
    # Execute INSERT query to input information into staff information table
    cursor.execute('''
        INSERT INTO staff_information (first_name, last_name, job_role)
        VALUES (?, ?, ?)
    ''', (first_name, last_name, job_role))
    # User inputs for staff account
    username = generate_username(first_name, last_name, "staff_accounts")
    print("Username:", username)
    password = get_valid_input("Enter password: ")
    print('Access Levels: 1-General, 5-Administrator')
    access_level = get_access_input("Enter access level: ")
    # Hash the password before storing it in staff accounts table
    hashed_password = hash_password(password)
    # Get the staff_id of the last inserted staff_information record
    staff_id = cursor.lastrowid
    # Insert staff account information into staff_accounts table
    cursor.execute('''
        INSERT INTO staff_accounts (username, password, access_level, staff_id)
        VALUES (?, ?, ?, ?)
    ''', (username, hashed_password, access_level, staff_id))
    # Commit changes and close the database
    connect.commit()
    connect.close()
def remove_staff():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User input for the staff ID to be removed
    staff_id = get_integer_input("Enter the staff ID to remove: ")
    # Check if the staff ID exists in staff_information
    cursor.execute('''
        SELECT * FROM staff_information WHERE staff_id = ?
    ''', (staff_id,))
    # Fetch result from SELECT query
    staff_info = cursor.fetchone()
    # If the staff account exists, proceed with confirmation
    if staff_info:
        # Display staff's first name and last name
        print(f"Removing staff: {staff_info[1]} {staff_info[2]}")
        # Prompt user for confirmation
        confirm = input("Enter 0 to cancel removal, or 1 to confirm removal: ")
        if confirm == "1":
            # Remove the corresponding row from staff_accounts
            cursor.execute('''
                DELETE FROM staff_accounts WHERE staff_id = ?
            ''', (staff_id,))
            # Remove the corresponding row from staff_information
            cursor.execute('''
                DELETE FROM staff_information WHERE staff_id = ?
            ''', (staff_id,))
            # Commit changes to the database
            connect.commit()
            connect.close()
            print(f"Staff with ID {staff_id} successfully removed.")
        else:
            print("Removal canceled.")
    else:
        print(f"Staff with ID {staff_id} not found.")
def view_staff_accounts():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # Perform a JOIN operation to retrieve information from both tables
    cursor.execute('''
        SELECT si.staff_id, sa.username, sa.access_level, si.first_name, si.last_name, si.job_role
        FROM staff_accounts sa
        JOIN staff_information si ON sa.staff_id = si.staff_id
    ''')
    # Fetch all the rows
    accounts = cursor.fetchall()
    # Display the retrieved information
    if accounts:
        print("| {:<10} | {:<25} | {:<12} | {:<20} | {:<20} | {:<20} |".format(
            "Staff ID", "Username", "Access Level", "First Name", "Last Name", "Job Role"))
        print("|" + "-" * 124 + "|")
        for account in accounts:
            print("| {:<10} | {:<25} | {:<12} | {:<20} | {:<20} | {:<20} |".format(
                account[0], account[1], account[2], account[3], account[4], account[5]))
        print("|" + "-" * 124 + "|")
    else:
        # Error handling if no accounts in table
        print("No accounts found.")
    connect.close()
def change_password(account_type):
    # Fetch global variable for current user logged in
    global current_user
    connect, cursor = database_connection()
    # Get the current password from the user
    current_password = get_valid_input("Please enter your current password: ")
    hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()
    # Check if the entered current password is correct
    cursor.execute(f'SELECT * FROM {account_type} WHERE username=? AND password=?', (current_user, hashed_current_password))
    user = cursor.fetchone()
    # If the details do not match, exit password change
    if user is None:
        print("Incorrect password. Password change failed.")
    else:
        # If the current password is correct, prompt for a new password
        new_password = get_valid_input("Please enter your new password: ")
        new_hashed_password = hash_password(new_password)
        # Prompt for the new password again for confirmation
        confirm_password = get_valid_input("Please confirm your new password: ")
        confirm_hashed_password = hash_password(confirm_password)
        # Check if the new passwords match
        if new_hashed_password != confirm_hashed_password:
            print("Passwords do not match. Password change failed.")
        else:
            # Update the password in the database
            cursor.execute(f'''
                UPDATE {account_type}
                SET password = ?
                WHERE username = ?
            ''', (new_hashed_password, current_user))
            print("Password successfully changed.")
    # Commit changes to the database and close the connection
    connect.commit()
    connect.close()
def reset_user_password():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # Prompt options for type of user requiring password reset
    print("Resest Password for: 1-Staff")
    user_choice = get_integer_input("Please select an option: ")
    # Set account type variable for SELECT and UPDATE query
    if user_choice == 1:
        account_type = "staff_accounts"
    else:
        print("Please select a valid option")
    username = get_valid_input("Please enter username of Account: ")
    # Fetch the current username and password
    cursor.execute(f'''
        SELECT username, password
        FROM {account_type}
        WHERE username = ?
    ''', (username,))
    # Fetch result from SELECT query
    result = cursor.fetchone()
    # If there is an account, proceed with password reset
    if result:
        username, password = result
        print(f"Resetting password for user: {username}")
        # User input for new user password
        new_password = get_valid_input("Enter the new password: ")
        new_hashed_password = hash_password(new_password)
        # Execute an SQL UPDATE statement to modify the password of the specified user
        cursor.execute(f'''
            UPDATE {account_type}
            SET password = ?
            WHERE username = ?
        ''', (new_hashed_password, username))
        # Commit changed and close database        
        connect.commit()
        connect.close()
        # Display changes and Error handling for invalid account
        print(f"User: {username} password changed to {new_password}")
    else:
        print(f"User: {username} not found.")
def change_access_level():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    username = get_valid_input("Please Enter Username: ")
    # Fetch the current username and access level
    cursor.execute('''
        SELECT username, access_level
        FROM staff_accounts
        WHERE username = ?
    ''', (username,))
    # Fetch result from SELECT query
    result = cursor.fetchone()
    # If an account exists, proceed with changing access level
    if result:
        username, current_access = result
        print('Access Levels: 1-General, 5-Administrator')
        print(f"Access Level of {username} is: {current_access}")
        # User input for new user access level
        new_access = get_access_input("Enter the new access level: ")
        # Execute an SQL UPDATE statement to modify the access level of the specified user
        cursor.execute('''
            UPDATE staff_accounts
            SET access_level = ?
            WHERE username = ?
        ''', (new_access, username))
        # Commit changes to the database and close the database connection
        connect.commit()
        connect.close()
        # Display changes to user
        print(f"User: {username} access level adjusted from {current_access} to {new_access}")
    else:
        print(f"User: {username} not found.")
def customer_register():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User inputs for customer information
    first_name = get_valid_input("Enter first name: ")
    last_name = get_valid_input("Enter last name: ")
    email = get_valid_input("Enter email address: ")
    # Execute INSERT query to input information into customer information table
    cursor.execute('''
        INSERT INTO customer_information (first_name, last_name, email)
        VALUES (?, ?, ?)
    ''', (first_name, last_name, email))
    # User inputs for customer account
    username = generate_username(first_name, last_name, "customer_accounts")
    print("Username:", username)
    password = get_valid_input("Enter password: ")
    # Hash the password before storing it in staff accounts table
    hashed_password = hash_password(password)
    # Get the cstomer_id of the last inserted customer_information record
    customer_id = cursor.lastrowid
    # Insert customer account information into customer_accounts table
    cursor.execute('''
        INSERT INTO customer_accounts (username, password, customer_id)
        VALUES (?, ?, ?)
    ''', (username, hashed_password, customer_id))
    # Commit changes to the database
    connect.commit()
    connect.close()
def remove_customer():
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User input for the customer ID to be removed
    customer_id = get_integer_input("Enter the Customer ID to remove: ")
    # Check if the customer ID exists in customer_information
    cursor.execute('''
        SELECT * FROM customer_information WHERE customer_id = ?
    ''', (customer_id,))
    # Fetch result from SELECT query
    customer_info = cursor.fetchone()
    # If the customer account exists, proceed with confirmation
    if customer_info:
        # Display customers's first name and last name
        print(f"Removing Customer: {customer_info[1]} {customer_info[2]}")
        # Prompt user for confirmation
        confirm = input("Enter 0 to cancel removal, or 1 to confirm removal: ")
        if confirm == "1":
            # Remove the corresponding row from customer_accounts
            cursor.execute('''
                DELETE FROM customer_accounts WHERE customer_id = ?
            ''', (customer_id,))
            # Remove the corresponding row from customer_information
            cursor.execute('''
                DELETE FROM customer_information WHERE customer_id = ?
            ''', (customer_id,))
            # Commit changes to the database
            connect.commit()
            connect.close()
            print(f"Customer with ID {customer_id} successfully removed.")
        else:
            print("Removal canceled.")
    else:
        print(f"Customer with ID {customer_id} not found.")
def view_customer_accounts():
    connect, cursor = database_connection()
    # Perform a JOIN operation to retrieve information from both tables
    cursor.execute('''
        SELECT ca.customer_id, ca.username, ci.first_name, ci.last_name, ci.email
        FROM customer_accounts ca
        JOIN customer_information ci ON ca.customer_id = ci.customer_id
    ''')

    # Fetch all the rows
    accounts = cursor.fetchall()

    # Display the retrieved information
    if accounts:
        print("| {:<12} | {:<25} | {:<20} | {:<20} | {:<30} |".format(
            "Customer ID", "Username", "First Name", "Last Name", "Email"))
        print("|" + "-" * 121 + "|")

        for account in accounts:
            print("| {:<12} | {:<25} | {:<20} | {:<20} | {:<30} |".format(
                account[0], account[1], account[2], account[3], account[4]))
        print("|" + "-" * 121 + "|")
    else:
        print("No accounts found.")
    
    # Don't forget to close the connection
    connect.close()

# Functions for main menus and sub menus
def staff_main_menu():
    # Print Application Name and staff options to users for input
    print('''Library Management System\n
            Welcome to the Staff Portal.\n
            1. View All Books
            2. Add New Book
            3. Delete Book
            4. Update Book Quantity
            5. Update Book Information
            6. Check Book Stock Status
            7. Admin Functions
            0. Exit
          
            \n\nCurrent user: ''',current_user
         )
    while True:
        # Displays staff main menu and prompts user choice input
        choice = get_integer_input("Enter your choice 0-6: ")

        if choice == 0:
            # Exit Program
            print("Exiting Program. Goodbye!")
            break
        elif choice == 1:
            # View all books in the library
            view_all_books()
        elif choice == 2:
            # Add a new book to the library
            add_book()
        elif choice == 3:
            # Remove a book from the library
            remove_book()
        elif choice == 4:
            # Update the quantity of a book in the library
            update_book_quantity()
        elif choice == 5:
            # Update the information of a book in the library
            update_book_information()
        elif choice == 6:
            # Check the stock status of a book in the library
            check_book_status()
        elif choice == 7:
            admin_menu()
        else:
            print("Please select a valid option.")
def admin_menu():
    # Fetch global variable for username of current user
    global current_user
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # SELECT query to check access level of logged in account
    cursor.execute('''
        SELECT access_level
        FROM staff_accounts
        WHERE username = ?
    ''', (current_user,))
    # Fetch the result of the SELECT query
    result = cursor.fetchone()
    # Check if there is a current user and their access level is 5
    if  result and result[0] == 5:
        # Print options to the user
        while True:
            print('''\nAdministration Options:
            0: Main Menu
            1: Add Staff Account
            2: Remove Staff Account
            3: Change User Access Level
            4: Change Password
            5: Reset User Password 
            6: View Staff Accounts
            7: View Customer Accounts
            8: Remove Customer Account      
                  ''')
            user_option = get_integer_input("Please select an option: ")
            # Admin function options
            if user_option == 0:
                break
            elif user_option == 1:
                print('Creating a New Staff Account')
                staff_register()
            elif user_option == 2:
                print('Removing a User:')
                remove_staff()
            elif user_option == 3:
                print('Changing user access level:')
                change_access_level()
            elif user_option == 4:
                change_password("staff_accounts")
            elif user_option == 5:
                reset_user_password()
            elif user_option == 6:
                view_staff_accounts()
            elif user_option == 7:
                view_customer_accounts()
            elif user_option == 8:
                remove_customer()
            else:
                # Error handling for incorrect option
                print('Please enter a valid option')
    else:
        # Error handling for account without permissions
        print("You do not have permission to access to access these functions")
def customer_main_menu():
    
    while True:
        # Print Application Name and staff options to users for input
        print('''Library Management System\n
                Welcome to the Customer Portal.\n
                1. View Available Books
                2. View Loans
                3. Change Password
                0. Logout

                \n\nCurrent user: ''',current_user
            )
        # Displays staff main menu and prompts user choice input
        choice = get_integer_input("Enter your choice 0-6: ")

        if choice == 0:
            # Exit Program
            print("Exiting Program. Goodbye!")
            break
        elif choice == 1:
            view_available_books()
        elif choice == 2:
            view_loans()
        elif choice == 3:
            change_password("customer_accounts")
        else:
            print("Please select a valid option.")

# Library Functions for books - Staff Functions
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
def remove_book():
    # Creates connection with SQLite3 database and creates cursor object
    connect, cursor = database_connection()
    book_id = get_integer_input("Please Enter Book ID: ")
    # Check if the book with the specified ID exists
    cursor.execute('SELECT title FROM books WHERE book_id = ?', (book_id,))
    result = cursor.fetchone()
    if result:
        while True:
            print(f"Please confirm removal of: {result[0]}\n 0: No, 1: Yes")
            # User input for removal confirmation
            user_choice = get_integer_input("Please select an option: ")
            if user_choice == 0:
                break
            elif user_choice == 1:
            # Book found, proceed with deletion, commit changes and print deletion confirmation to the user
                cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
                connect.commit() 
                print(f"{result[0]} removed from the library")
                break
            else:
                 # Error handling for invalid option
                print('Invalid option. Please enter 0 or 1.')
        else:
            # Error handling for book not found in table
            print(f"No book found with ID: {book_id}")
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
        # Display current quantity and input for new book quantity
        print(f"The current quantity of {result[0]} is: {result[1]}")
        new_quantity = get_integer_input("Please Enter New Quantity: ")
        # Update the quantity of the specified book
        cursor.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))
        print(f"Quantity for {result[0]} updated from {result[1]} to {new_quantity}.")
    else:
        # Error handling for book not found in table
        print(f"No book found with ID: {book_id}")
    # Commit changes and close the database connection
    connect.commit()
    connect.close()
def update_book_information():
     # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    book_id = get_integer_input("Please Enter Book ID: ")
    # Check if book exists in table and fetch result
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    result = cursor.fetchone()
    # If book exists, prompt user input for new book information
    if result:
        # Display current information for selected book
        print(f"Make changes to ID:{book_id} {result[1]} by {result[2]}: ")
        print(f"Current Information:\n ID: {book_id}, Title: {result[1]}, Author: {result[2]}\nISBN: {result[3]}, Pub Date:{result[4]}, Genre: {result[5]}\n ")
        # User input for new book information
        new_title = get_valid_input("Please Enter New Title: ")
        new_author = get_valid_input("Please Enter New Author: ")
        new_isbn = get_valid_input("Please Enter New ISBN: ")
        new_pub_date = get_valid_input("Please Enter New Publication Date(YYYY-MM-DD): ")
        new_genre = get_valid_input("Please Enter New Genre: ")
        # Execute an UPDATE statement to modify the quantity of the specified item
        cursor.execute('''
            UPDATE books
            SET title = ?, author = ?, isbn = ?, pub_date = ?, genre = ?
            WHERE book_id = ?
            ''', (new_title, new_author, new_isbn, new_pub_date, new_genre, book_id))
        # Execute a SELECT query to fetch updated book information
        cursor.execute('''
                SELECT *
                FROM books
                WHERE book_id = ?
            ''', (book_id,))
        updated_details = cursor.fetchone()
        print(f"Updated information for: {updated_details[1]}:")
        # Print the updated details in a formatted table
        print("{:<5} {:<25} {:20} {:<15} {:<12} {:<30}".format("ID", "Name", "Author", "ISBN", "Date", "Description"))
        print("From:")
        print("{:<5} {:<25} {:<20} {:<15} {:<12} {:<30}".format(*result))
        print("To:")
        # Print updated details
        print("{:<5} {:<25} {:<20} {:<15} {:<12} {:<30}".format(*updated_details))
    else:
        # Error handling for book not found in table
        print(f"No book found with ID: {book_id}")
    # Commit changes to database and close database connection
    connect.commit()
    connect.close()
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

# Library Functions for books - Customer Functions
def view_available_books():
    # Creates connection with SQLite3 database and creates cursor object
    connect, cursor = database_connection()
    # Execute a SELECT query to retrieve columns and data from the books table
    cursor.execute('''
        SELECT book_id, title, author, isbn, pub_date, genre, quantity
        FROM books
        WHERE quantity >= 1
    ''')
    # Fetch all results obtained from SELECT query
    books = cursor.fetchall()
    # Close SQLite3 database connection
    connect.close()
    # Check if there are any books in the books table
    if books:
        # If there are books, print a header for the book information to the user
        print("Books in the Library with Quantity of 1 or More:")
        # Print a formatted header with column names to the user
        print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format("ID", "Title", "Author", "ISBN", "Date", "Genre", "QTY"))
        print("|" + "-" * 154 + "|")
        for book in books:
        # Print formatted information for each book in books table
            print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format(*book))
        print("|" + "-" * 154 + "|")

        while True:
            print("Options: 0-Main Menu, 1-Borrow Book")
            user_choice = get_integer_input("Please select an option: ")
            if user_choice == 0:
                break
            elif user_choice == 1:
                borrow_book()
            else:
                print("Please select a valid option")
    else:
    # Error handling if no data in books table
        print("No books available")
def view_loans():
    global current_user
    connect, cursor = database_connection()
    # Get the customer_id based on the current username
    cursor.execute('''
        SELECT customer_id FROM customer_accounts WHERE username = ?
    ''', (current_user,))
    customer_id = cursor.fetchone()[0]

    # Query to retrieve all books on loan for the current customer
    cursor.execute('''
        SELECT transactions.transaction_id, books.book_id, books.title, books.author, transactions.borrow_date, transactions.return_date
        FROM transactions
        INNER JOIN books ON transactions.book_id = books.book_id
        WHERE transactions.customer_id = ? AND transactions.date_returned IS NULL
        
    ''', (customer_id,))
        # Fetch all rows from the result set
    loans = cursor.fetchall()

    
    connect.close()

    if loans: 
        print("Current Books on Loan: ")  
        # Print formatted table header
        print("| {:<8} | {:<8} | {:<45} | {:<25} | {:<15} | {:<15} |".format(
            "Trans ID", "Book ID", "Title", "Author", "Borrow Date", "Return Date"))
        print("|" + "-" * 133 + "|")

        # Print formatted table rows
        for book in loans:
            print("| {:<8} | {:<8} | {:<45} | {:<25} | {:<15} | {:<15} |".format(
                book[0], book[1], book[2], book[3], book[4], book[5]))
        print("|" + "-" * 133 + "|")
        
        while True:
            print("Options: 0-Main Menu, 1-Return Book")
            user_choice = get_integer_input("Please select an option: ")
            if user_choice == 0:
                break
            elif user_choice == 1:
                return_book()
            else:
                print("Please select a valid option")
    else:
        print("No books currently on loan")
def borrow_book():
    global current_user
    connect, cursor = database_connection()
    cursor.execute('SELECT customer_id FROM customer_accounts WHERE username = ?', (current_user,))
    result = cursor.fetchone()
    customer_id = result[0]
    book_id = get_integer_input("Please enter the ID of book to borrow: ")
    # Check if the book is available (quantity > 0)
    cursor.execute('SELECT quantity FROM books WHERE book_id = ?', (book_id,))
    result = cursor.fetchone()
    if result is not None and result[0] > 0:
        # Book is available, proceed with the transaction
        borrow_date = datetime.now().strftime('%Y-%m-%d')
        return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')  # Assuming a 14-day borrowing period
        # Insert the transaction record
        cursor.execute('''
            INSERT INTO transactions (customer_id, book_id, borrow_date, return_date)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, book_id, borrow_date, return_date))
        # Update the book quantity (subtract 1)
        cursor.execute('UPDATE books SET quantity = quantity - 1 WHERE book_id = ?', (book_id,))
        # Commit the changes to the database
        connect.commit()
        print(f"Book borrowed successfully. Return by: {return_date}")
    else:
        print("Sorry, the book is not available for borrowing.")
def return_book():
    connect, cursor = database_connection()
    transaction_id = get_integer_input("Please enter transaction ID: ")
    # Check if the transaction ID is valid
    cursor.execute('SELECT * FROM transactions WHERE transaction_id = ?', (transaction_id,))
    transaction = cursor.fetchone()
    if transaction is not None and transaction[5] is None:  # Check if the book has not been returned already
        # Update the transaction record with the return date
        return_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            UPDATE transactions
            SET date_returned = ?
            WHERE transaction_id = ?
        ''', (return_date, transaction_id))
        # Update the book quantity (add 1)
        cursor.execute('UPDATE books SET quantity = quantity + 1 WHERE book_id = ?', (transaction[2],))
        # Commit the changes to the database
        connect.commit()
        connect.close()
        print("Book returned successfully.")
        view_loans()
    elif transaction is not None and transaction[4] is not None:
        print("Book has already been returned.")
    else:
        print("Invalid transaction ID.")


if __name__ == "__main__":
    # Create tables in database if they do not exist
    create_tables()
    # Create an admin account for first time use
    create_admin()
    while True:
        main_menu()
        user_choice = get_integer_input("Please select an option: ")
        if user_choice == 0:
            break
        # Staff Login Portal with options
        elif user_choice == 1:
            while True:
                print('''Library Management System\n
                    Welcome to the Staff Portal.\n
                    1. Login
                    0. Return to Main Menu
                 ''')
                staff_choice = get_integer_input("Please select an option: ")
                # Return to main menu
                if staff_choice == 0:
                    break
                # Login page for staff accounts
                elif staff_choice == 1:
                    login("staff_accounts")
                else:
                    # Error handling for invald option selected
                    print("Please select a valid option")
        elif user_choice == 2:
            while True:
                print('''Library Management System\n
                    Welcome to the Customer Portal.\n
                    1. Login
                    2. Register
                    0. Return to Main Menu
                 ''')
                customer_choice = get_integer_input("Please select an option: ")

                if customer_choice == 0:
                    break
                elif customer_choice == 1:
                    login("customer_accounts")
                elif customer_choice == 2:
                    customer_register()
                else:
                    print("Please select a valid option")
        else:
            print("Please select a valid option")