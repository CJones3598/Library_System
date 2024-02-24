# Import SQLite3 module and Error class for database functionality
import sqlite3
from sqlite3 import Error
# Import hashlib module for password hashing
import hashlib
# Import random module for username creation
import random
# Import datetime and timedelta class from datetime module for transactions
from datetime import datetime, timedelta
# Import os module for clearing screen
import os
# Import time module for pauses before clearing the screen
import time

# Global variables for username of user logged in
current_user = None

# Functions for input validations
def get_valid_input(prompt):
    while True:
        # Get user input, remove leading/trailing whitespaces, and convert to uppercase
        user_input = input(prompt).strip().upper()
        # Check if the input is non-empty
        if user_input:
            # If valid, return value
            return user_input
        else:
            # Error handling for invalid input
            print("Invalid Input.")
def get_integer_input(prompt):
    while True:
        try:
            # Check if user input is an integer, if integer return value
            user_input = int(input(prompt))
            return user_input
        # If value not integer, return an error and prompt input
        except ValueError:
            print("Invalid Input")
def get_access_input(prompt):
    while True:
        try:
            # Check if user input is an integer
            user_input = int(input(prompt))
            # Check if the input is either 1 or 5
            if user_input in [1, 5]:
                return user_input
            else:
                print("Invalid Input.")
        except ValueError:
            print("Invalid Input.")

# Functions to connect to SQLite3 database and create tables in database
def database_connection():
    # Creates connection with SQLite3 database and creates cursor object
    connect = sqlite3.connect('library.db')
    cursor = connect.cursor()
    # Execute foreign key setting
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

# Functions for main menus and sub menus
def main_menu():
    # Print main menu options
    print('''Library Management System\n
                    Welcome to the library management system.\n
                    1: Staff Portal
                    2: Customer Portal
          
                    0: Exit Program
                ''')
def staff_main_menu():
     while True:
        clear_screen()
        # Print Application Name and staff options to users for input
        print('''Library Management System\n
                Welcome to the Staff Portal.\n
                1: View All Books
                2: Add New Book
                3: Delete Book
                4: Update Book Quantity
                5: Update Book Information
                6: Check Book Stock Status
                7: View All Loans
                8: Admin Functions
                9: Change Password
                0: Logout
            
                \n\nCurrent user: ''',current_user
            )
        # Displays staff main menu and prompts user choice input
        staff_choice = get_integer_input("Select an Option: ")

        if staff_choice == 0:
            # Exit Program
            print("Logging Out. Goodbye!")
            time.sleep(2)
            break
        elif staff_choice == 1:
            # View all books in the library
            view_all_books()
        elif staff_choice == 2:
            # Add a new book to the library
            add_book()
        elif staff_choice == 3:
            # Remove a book from the library
            remove_book()
        elif staff_choice == 4:
            # Update the quantity of a book in the library
            update_book_quantity()
        elif staff_choice == 5:
            # Update the information of a book in the library
            update_book_information()
        elif staff_choice == 6:
            # Check the stock status of a book in the library
            check_book_status()
        elif staff_choice == 7:
            # View all books on loan
            view_all_loans()
        elif staff_choice == 8:
            # Administrator Menu for admin functions
            admin_menu()
        elif staff_choice == 9:
            # Change password for user logged in
            change_password("staff_accounts")
        else:
            # Error Handling for invalid input
            print("Invalid Option.")
            time.sleep(2)
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
            clear_screen()
            print('''Administration Options:\n
                    View Accounts:
                        1: Staff Accounts
                        2: Customer Accounts
                    Staff Account Management:
                        3: Add Staff Account
                        4: Remove Staff Account
                        5: Change User Access Level
                    Customer Account Management:
                        6: Add Customer Account
                        7: Remove Customer Account
                    Password Management:
                        8: Reset User Password\n
      
                        0: Main Menu\n''')
            admin_option = get_integer_input("Select an Option: ")
            # Return to main menu
            if admin_option == 0:
                break
            # View all staff accounts and information
            elif admin_option == 1:
                view_staff_accounts()
            # View all customer accounts and information
            elif admin_option == 2:
                view_customer_accounts()
            # Create a new staff account
            elif admin_option == 3:
                staff_register()
            # Remove a staff account
            elif admin_option == 4:
                remove_staff()
            # Change the access level of a staff member
            elif admin_option == 5:
                change_access_level()
            # Create a new customer account
            elif admin_option == 6:
                customer_register()
            # Remove a customer account
            elif admin_option == 7:
                remove_customer()
            # Change the password of a selected user account
            elif admin_option == 8:
                reset_user_password()
            else:
                # Error handling for incorrect option
                print('Invalid Option.')
                time.sleep(2)
    else:
        # Error handling for account without permissions
        print("You do not have permission to access to access these functions")
        time.sleep(2)
def customer_main_menu():
    while True:
        clear_screen()
        # Print Application Name and staff options to users for input
        print('''Library Management System\n
                Welcome to the Customer Portal.\n
                1: View Available Books
                2: View Loans
                3: Change Password
                0: Logout

                \n\nCurrent user: ''',current_user
            )
        # Displays staff main menu and prompts user choice input
        customer_choice = get_integer_input("Select an Option: ")
        # Exit Program
        if customer_choice == 0:
            print("Logging out. Goodbye!")
            time.sleep(2)
            break
        # View all available books and borrow books
        elif customer_choice == 1:
            view_available_books()
        # View all loans and returns for customer logged in 
        elif customer_choice == 2:
            view_loans()
        # Change password for user logged in
        elif customer_choice == 3:
            change_password("customer_accounts")
        else:
            # Error handling for invalid input
            print("Invalid Option.")
            time.sleep(2)
def options_menu():
    # Print options to user
    while True:
        print('\nOptions: \n0:Main Menu, 1:View All, 2:Borrow Book, 3:Sort, 4:Filter')
        user_option = get_integer_input("Select an Option: ")
        # Return to main menu
        if user_option == 0:
            break
        # View all available books in library
        elif user_option == 1:
            view_available_books()
            break
        # Borrow a book from the library
        elif user_option == 2:
            borrow_book()
            view_available_books()
            break
        # Sort available books in library
        elif user_option == 3:
            print('''Attribute: 1:Title, 2:Author, 3:ISBN, 4:Pub Date, 5:Genre, 6:Quantity\nSort Order: 1: Ascending, 2: Descending ''')
            attribute = get_integer_input("Enter attribute to sort by: ")
            order = get_integer_input("Enter order to sort by: ")
            clear_screen()
            sort_books(attribute, order, 'quantity >=1')
        # Filter available books in library
        elif user_option == 4:
            print('''Attribute: 1:Title, 2:Author, 3:ISBN, 4:Pub Date, 5:Genre''')
            filter_attribute = get_integer_input("Enter attribute to filter by: ")
            filter_value = input("Enter value to filter by: ")
            clear_screen()
            filter_books(filter_attribute, filter_value)
        else:
            # Error handling for invalid option
            print('Invalid Option')
            time.sleep(2)

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
    # Fetch global variable for the username of the current logged-in user
    global current_user
    # Creates a connection with the SQLite3 database and creates a cursor object
    connect, cursor = database_connection()
    # Create a variable for login attempts
    attempts = 0
    # Login block for more than 5 invalid logins
    while attempts < 5:
        clear_screen()
        print("Library System Login: \n Enter 'exit' to exit to Main Menu\n")
        # Take user input for username and password
        username = get_valid_input("Enter Username: ")
        # Error handling to cancel login
        if username.lower() == 'exit':
            print("Login Cancelled. Returning to Main Menu.")
            time.sleep(2)
            return False
        password = get_valid_input("Enter Password: ")
        # Hash the password for comparison
        hashed_password = hash_password(password)
        # Check if the username and hashed password match in relevant accounts table
        cursor.execute(f'SELECT * FROM {account_type} WHERE username=? AND password=?', (username, hashed_password))
        # Fetch the result from the SELECT query
        account = cursor.fetchone()
        # If the account is valid, proceed with login
        if account:
            print("Login Successful.")
            time.sleep(2)
            current_user = username
            return True
        else:
            # Login Block calculations for attempts
            attempts += 1
            remaining_attempts = 5 - attempts
            print(f"Invalid username or password. Remaining attempts: {remaining_attempts}")
            time.sleep(2)
            # Maximum Login attempt handling
            if attempts >= 5:
                print("Exceeded maximum login attempts. Closing the program.")
                time.sleep(2)
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
        cursor.execute('INSERT INTO staff_information VALUES (?, ?, ?, ?)', ("1", "admin", "admin", "admin"))
        cursor.execute('INSERT INTO staff_accounts VALUES (?, ?, ?, ?)', (username, hashed_password, "5", "1"))
        print("Administrator account created with username 'ADMIN' and password 'ADMIN'\nPlease change the password after login.")
        # Commit the changes and close the connection to SQLite database
        connect.commit()
        connect.close()
def staff_register():
    clear_screen()
    print("Creating New Staff Account: \n")
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User inputs for staff information
    first_name = get_valid_input("Enter First Name: ")
    last_name = get_valid_input("Enter Last Name: ")
    job_role = get_valid_input("Enter Job Role: ")
    # Execute INSERT query to input information into staff information table
    cursor.execute('''
        INSERT INTO staff_information (first_name, last_name, job_role)
        VALUES (?, ?, ?)
    ''', (first_name, last_name, job_role))
    # User inputs for staff account
    username = generate_username(first_name, last_name, "staff_accounts")
    print("Username:", username)
    password = get_valid_input("Enter Password: ")
    print('Access Levels: 1:General, 5:Administrator')
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
    clear_screen()
    print("Removing staff member: \n")
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User input for the staff ID to be removed
    staff_id = get_integer_input("Enter Staff ID: ")
    # Check if the staff ID exists in staff_information
    cursor.execute('''
        SELECT * FROM staff_information WHERE staff_id = ?
    ''', (staff_id,))
    # Fetch result from SELECT query
    staff_info = cursor.fetchone()
    # If the staff account exists, proceed with confirmation
    if staff_info:
        # Display staff's first name and last name
        print(f"Removing Staff: {staff_info[1]} {staff_info[2]}")
        # Prompt user for confirmation
        confirm = input("Enter 0 to cancel, or 1 to confirm: ")
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
            print(f"Staff: {staff_id} {staff_info[1]} {staff_info[2]} successfully removed.")
            time.sleep(2)
        else:
            print("Removal cancelled.")
            time.sleep(2)
    else:
        print(f"Staff ID {staff_id} not found.")
        time.sleep(2)
def view_staff_accounts():
    clear_screen()
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
        while True:
            print('\nOptions:\n0:Main Menu')
            user_option = get_integer_input("Select an Option: ")
            # Exit the loop when 0 is selected and return to main menu
            if user_option == 0:
                break
            else:
                print("Invalid Option")
    else:
        # Error handling if no accounts in table
        print("No accounts found.")
        time.sleep(2)
    connect.close()
def change_password(account_type):
    clear_screen()
    print("Changing Password: \n")
    # Fetch global variable for current user logged in
    global current_user
    connect, cursor = database_connection()
    # Get the current password from the user
    current_password = get_valid_input("Enter current password: ")
    hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()
    # Check if the entered current password is correct
    cursor.execute(f'SELECT * FROM {account_type} WHERE username=? AND password=?', (current_user, hashed_current_password))
    user = cursor.fetchone()
    # If the details do not match, exit password change
    if user is None:
        print("Incorrect password. Password change failed.")
        time.sleep(3)
    else:
        # If the current password is correct, prompt for a new password
        new_password = get_valid_input("Enter new password: ")
        new_hashed_password = hash_password(new_password)
        # Prompt for the new password again for confirmation
        confirm_password = get_valid_input("Re-enter new password: ")
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
            time.sleep(2)
    # Commit changes to the database and close the connection
    connect.commit()
    connect.close()
def reset_user_password():
    #clear_screen()
    print("Changing password for user: \n")
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # Prompt options for type of user requiring password reset
    print("Resest Password for: 1:Staff, 2:Customer")
    user_choice = get_integer_input("Select an Option: ")
    # Set account type variable for SELECT and UPDATE query
    if user_choice == 1:
        account_type = "staff_accounts"
    elif user_choice == 2:
        account_type = "customer_accounts"
    else:
        print("Invalid Option")
    username = get_valid_input("Enter Account Username: ")
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
        print(f"Resetting password for: {username}")
        # User input for new user password
        new_password = get_valid_input("Enter new password: ")
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
        time.sleep(2)
    else:
        print(f"User: {username} not found.")
        time.sleep(2)
def change_access_level():
    clear_screen()
    print("Changing access level for a staff member: \n")
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    username = get_valid_input("Enter Username: ")
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
        print("Access Levels: 1-General, 5-Administrator")
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
        time.sleep(2)
    else:
        print(f"User: {username} not found.")
        time.sleep(2)
def customer_register():
    clear_screen()
    print("Creating new customer account: \n")
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
    print("Register Account Successful. Welcome", first_name)
    time.sleep(2)
    # Commit changes to the database
    connect.commit()
    connect.close()
def remove_customer():
    clear_screen()
    print("Removing a customer account: \n")
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User input for the customer ID to be removed
    customer_id = get_integer_input("Enter Customer ID: ")
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
        confirm = input("Enter 0 to cancel, or 1 to confirm: ")
        if confirm == "1":
            # Remove the corresponding transactions from the transactions table
            cursor.execute('''
                DELETE FROM transactions WHERE customer_id = ?
            ''', (customer_id,))
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
            print(f"Customer: {customer_id} {customer_info[1]} {customer_info[2]} and associated transactions successfully removed.")
            time.sleep(2)
        else:
            print("Removal cancelled.")
            time.sleep(2)

    else:
        print(f"Customer ID {customer_id} not found.")
        time.sleep(2)
def view_customer_accounts():
    clear_screen()
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
        while True:
            print('\nOptions:\n0:Main Menu')
            user_option = get_integer_input("Select an Option: ")
            # Exit the loop when 0 is selected and return to main menu
            if user_option == 0:
                break
            else:
                print("Invalid Option")
                time.sleep(2)
    else:
        print("No accounts found.")
        time.sleep(2)
    
    # Close the database connection
    connect.close()

# Library Functions for books - Staff Functions
def view_all_books():
    clear_screen()
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
        print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format("ID", "Title", "Author", "ISBN", "Date", "Genre", "QTY"))
        print("|" + "-" * 154 + "|")
        for book in books:
            # Print formatted information for each book in books table
            print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format(*book))
        print("|" + "-" * 154 + "|")
        # Print options to user
        while True:
            print('\nOptions: \n0:Main Menu, 1:View All, 2:Sort, 3:Filter')
            user_option = get_integer_input("Select an Option: ")
            # Return to main menu
            if user_option == 0:
                break
            # View all books in library
            elif user_option == 1:
                view_all_books()
                break
            # Sort books in libary
            elif user_option == 2:
                print('''Attribute: 1:Title, 2:Author, 3:ISBN, 4:Pub Date, 5:Genre, 6:Quantity\nSort Order: 1: Ascending, 2: Descending ''')
                attribute = get_integer_input("Enter attribute to sort by: ")
                order = get_integer_input("Enter order to sort by: ")
                clear_screen()
                sort_books(attribute, order, 'quantity >=1')
            # Filter books in library
            elif user_option == 3:
                print('''Attribute: 1:Title, 2:Author, 3:ISBN, 4:Pub Date, 5:Genre''')
                filter_attribute = get_integer_input("Enter the attribute to filter by: ")
                filter_value = input("Enter the value to filter by: ")
                clear_screen()
                filter_books(filter_attribute, filter_value)
            else:
                # Error handling for incorrect option
                print('Invalid Option')
                time.sleep(2)
    else:
        # Error handling if no data in books table
        print("No books found in the library.")
        time.sleep(2)
def add_book():
    clear_screen()
    print("Adding New Book:\n")
    # Creates connection with SQLite3 database and creates cursor object
    connect, cursor = database_connection()
    # User input fields for adding new book to table
    title = get_valid_input("Enter Book Title: ")
    author = get_valid_input("Enter Book Author: ")
    isbn = get_valid_input("Enter Book ISBN: ")
    pub_date = get_valid_input("Enter Book Publication Date (YYYY-MM-DD): ")
    genre = get_valid_input("Enter Book Genre: ")
    quantity = get_integer_input("Enter Book Quantity: ")
    # Queries to insert new record into books table in database
    cursor.execute('''
        INSERT INTO books (title, author, isbn, pub_date, genre, quantity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, author, isbn, pub_date, genre, quantity))
    # Display data inserted into table to user
    print("Data inserted into table: ")
    last_added = cursor.execute('''SELECT * FROM books ORDER BY book_id DESC LIMIT 1''').fetchone()
        # Print a formatted header with column names to the user
    print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format("ID", "Title", "Author", "ISBN", "Date", "Genre", "QTY"))
    print("|" + "-" * 154 + "|")
    # Print formatted information for each book in books table
    print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format(*last_added))
    print("|" + "-" * 154 + "|")
    # Commit table and database changes and close connection
    connect.commit()
    connect.close()
    time.sleep(2)
def remove_book():
    clear_screen()
    print("Removing Book: \n ")
    # Creates connection with SQLite3 database and creates cursor object
    connect, cursor = database_connection()
    book_id = get_integer_input("Enter Book ID: ")
    # Check if the book with the specified ID exists
    cursor.execute('SELECT title FROM books WHERE book_id = ?', (book_id,))
    result = cursor.fetchone()
    if result:
        while True:
            print(f"Please confirm removal of: {result[0]}\nOptions: 0:No, 1:Yes")
            # User input for removal confirmation
            user_choice = get_integer_input("Select an Option: ")
            if user_choice == 0:
                print("Removal Cancelled")
                time.sleep(2)
                break
            elif user_choice == 1:
            # Book found, proceed with deletion, commit changes and print deletion confirmation to the user
                cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
                connect.commit() 
                print(f"{result[0]} removed from the library")
                time.sleep(2)
                break
            else:
                 # Error handling for invalid option
                print('Invalid Option.')
                time.sleep(2)
    else:
        # Error handling for book not found in table
        print(f"No book found with ID: {book_id}")
def update_book_quantity():
    clear_screen()
    print("Updating Book Quantity:\n ")
     # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # User input for book id
    book_id = get_integer_input("Enter Book ID: ")
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
        new_quantity = get_integer_input("Enter New Quantity: ")
        # Update the quantity of the specified book
        cursor.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))
        print(f"Quantity for {result[0]} updated from {result[1]} to {new_quantity}.")
        time.sleep(2)
    else:
        # Error handling for book not found in table
        print(f"No book found with ID: {book_id}")
        time.sleep(2)
    # Commit changes and close the database connection
    connect.commit()
    connect.close()
def update_book_information():
    clear_screen()
    print("Updating Book Information: \n")
     # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    book_id = get_integer_input("Enter Book ID: ")
    # Check if book exists in table and fetch result
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    result = cursor.fetchone()
    # If book exists, prompt user input for new book information
    if result:
        # Display current information for selected book
        print(f"Make changes to: {result[1]} by {result[2]}: ")
        print(f"Current Information:\nID: {book_id}, Title: {result[1]}, Author: {result[2]}\nISBN: {result[3]}, Pub Date:{result[4]}, Genre: {result[5]}\n ")
        # User input for new book information
        new_title = get_valid_input("Enter New Title: ")
        new_author = get_valid_input("Enter New Author: ")
        new_isbn = get_valid_input("Enter New ISBN: ")
        new_pub_date = get_valid_input("Enter New Publication Date(YYYY-MM-DD): ")
        new_genre = get_valid_input("Enter New Genre: ")
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
        time.sleep(2)
    else:
        # Error handling for book not found in table
        print(f"No book found with ID: {book_id}")
        time.sleep(2)
    # Commit changes to database and close database connection
    connect.commit()
    connect.close()
def check_book_status():
    clear_screen()
    print("Checking Book Stock Status: \n")
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
            time.sleep(2)
        else:
            print(f"Book: {result[0]} is Out of stock")
            time.sleep(2)
    else:
        # Error handling for book not found in table
        print(f"Book not found with ID: {book_id}")
        time.sleep(2)
def view_all_loans():
    clear_screen()
    connect, cursor = database_connection()
    # Query to retrieve all books on loan for all customers
    cursor.execute('''
        SELECT ci.customer_id, ci.first_name || ' ' || ci.last_name AS full_name, t.transaction_id, b.book_id, b.title, t.borrow_date, t.return_date
        FROM customer_information ci
        INNER JOIN transactions t ON ci.customer_id = t.customer_id
        INNER JOIN books b ON t.book_id = b.book_id
        WHERE t.date_returned IS NULL
    ''')
    # Fetch all rows from the result set
    loans = cursor.fetchall()
    connect.close()
    if loans:
     print("All Books on Loan:")
     print("| {:<10} | {:<25} | {:<10} | {:<8} | {:<45} | {:<15} | {:<15} |".format(
         "Cust. ID", "Customer", "Trans. ID", "Book ID", "Title", "Borrow Date", "Return Date"))
     print("|" + "-" * 148 + "|")
     for loan in loans:
         print("| {:<10} | {:<25} | {:<10} | {:<8} | {:<45} | {:<15} | {:<15} |".format(
             loan[0], loan[1], loan[2], loan[3], loan[4], loan[5], loan[6]))
     print("|" + "-" * 148 + "|")
     while True:
            print('\nOptions:\n0:Main Menu')
            user_option = get_integer_input("Select an Option: ")
            # Exit the loop when 0 is selected and return to main menu
            if user_option == 0:
                break
            else:
                print("Invalid Option")
                time.sleep(2)
    else:
      print("No books currently on loan.")
      time.sleep(2)

# Library Functions for books - Customer Functions
def view_available_books():
    clear_screen()
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
        options_menu()
    else:
        # Error handling if no data in books table
        print("No books available")
        time.sleep(2)
def view_loans():
    clear_screen()
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
    # Close database connection
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
            print("\nOptions:\n0:Main Menu, 1:Return Book")
            user_choice = get_integer_input("Select an Option: ")
            if user_choice == 0:
                break
            elif user_choice == 1:
                return_book()
                view_loans()
                break
            else:
                print("Invalid Option")
                time.sleep(2)
    else:
        print("No books currently on loan")
        time.sleep(2)
def borrow_book():
    global current_user
    connect, cursor = database_connection()
    cursor.execute('SELECT customer_id FROM customer_accounts WHERE username = ?', (current_user,))
    result = cursor.fetchone()
    customer_id = result[0]
    book_id = get_integer_input("Enter ID of book to borrow: ")
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
        time.sleep(2)
    else:
        print("Sorry, the book is not available for borrowing.")
        time.sleep(2)
def return_book():
    connect, cursor = database_connection()
    transaction_id = get_integer_input("Enter transaction ID: ")
    # Check if the transaction ID is valid
    cursor.execute('SELECT * FROM transactions WHERE transaction_id = ?', (transaction_id,))
    transaction = cursor.fetchone()
    # Check if the book has not been returned already
    if transaction is not None and transaction[5] is None:  
        # Update the transaction record with the return date
        return_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            UPDATE transactions
            SET date_returned = ?
            WHERE transaction_id = ?
        ''', (return_date, transaction_id))
        # Update the book quantity, add 1 to quantity
        cursor.execute('UPDATE books SET quantity = quantity + 1 WHERE book_id = ?', (transaction[2],))
        # Commit the changes to the database
        connect.commit()
        connect.close()
        print("Book returned successfully.")
        time.sleep(2)
    elif transaction is not None and transaction[4] is not None:
        print("Book has already been returned.")
        time.sleep(2)
    else:
        print("Invalid transaction ID.")
        time.sleep(2)

# Library Functions for sorting and filtering books - Staff & Customer Functions
def sort_books(attribute=1, order=1, condition=''):
    clear_screen()
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # Map numbers to sorting attributes and orders
    attribute_mapping = {1: 'title', 2: 'author', 3: 'isbn', 4: 'pub_date', 5: 'genre', 6: 'quantity'}
    order_mapping = {1: 'ASC', 2: 'DESC'}
    # Validate and set the sorting attribute
    if attribute not in attribute_mapping:
        print("Invalid sorting attribute. Defaulting to sorting by name.")
        attribute = 1
    # Validate and set the sorting order
    if order not in order_mapping:
        print("Invalid sorting order. Defaulting to ascending order.")
        order = 1
    # Assign values to be passed to SELECT query
    attribute_name = attribute_mapping[attribute]
    order_direction = order_mapping[order]
    # Add condition if provided
    if condition:
        condition = f' WHERE {condition}'
    # Execute a SELECT query to retrieve sorted columns from the books table
    cursor.execute(f'''
        SELECT book_id, title, author, isbn, pub_date, genre, quantity
        FROM books
        {condition}
        ORDER BY ({attribute_name}) {order_direction} 
    ''')
    # Fetch all results from SELECT query
    sorted_books = cursor.fetchall()
    # Close the database connection
    connect.close()
    # Display sorted data from SELECT query to the user
    print(f"Sorted Library by {attribute_name.upper()} ({order_direction.capitalize()}ending Order):")
    print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format("ID", "Title", "Author", "ISBN", "Date", "Genre", "QTY"))
    print("|" + "-" * 154 + "|")
    for book in sorted_books:
        # Print formatted information for each book in books table
        print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format(*book))
    print("|" + "-" * 154 + "|")
def filter_books(filter_attribute=1, filter_value=''):
    clear_screen()
    # Create a connection with the SQLite3 database and create a cursor object
    connect, cursor = database_connection()
    # Map numbers to filter attributes
    filter_mapping = {1: 'title', 2: 'author', 3: 'isbn', 4: 'pub_date', 5: 'genre'}
    # Validate and set the filtering attribute
    if filter_attribute not in filter_mapping:
        print("Invalid filter attribute. Defaulting to filter by name.")
        filter_attribute = 1
    # Assign values to be passed to SELECT query
    attribute_filter = filter_mapping[filter_attribute]
    # Execute a SELECT query to retrieve filtered columns from the books table
    cursor.execute(f'''
        SELECT * FROM books
        WHERE LOWER({attribute_filter}) LIKE ?
    ''', ('%' + filter_value.lower() + '%',))
    # Fetch all results from SELECT query
    filtered_books = cursor.fetchall()
    # Close the database connection
    connect.close()
    # Display sorted data from SELECT query
    if not filtered_books:
        print("No books found with the given filter.")
        time.sleep(2)
    else:
        print(f"Filter Library by {attribute_filter.upper()} for {filter_value.upper()}:")
        print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format("ID", "Title", "Author", "ISBN", "Date", "Genre", "QTY"))
        print("|" + "-" * 154 + "|")
        for book in filtered_books:
        # Print formatted information for each book in books table
            print("| {:<5} | {:<45} | {:<28} | {:<15} | {:<12} | {:<25} | {:<4} |".format(*book))
        print("|" + "-" * 154 + "|")

# Utility Functions
def clear_screen():
    # Clear screen command for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear screen command for Linux and macOS
    else:
        os.system('clear')

if __name__ == "__main__":
    # Create tables in database if they do not exist
    create_tables()
    # Create an admin account for first time use
    create_admin()
    while True:
        clear_screen()
        main_menu()
        # User input for selecting options
        user_choice = get_integer_input("Select an Option: ")
        # Exit Program
        if user_choice == 0:
            print("Exiting Program.")
            time.sleep(2)
            break
        # Staff Login Portal with options
        elif user_choice == 1:
            while True:
                clear_screen()
                print('''Library Management System\n
                    Welcome to the Staff Portal.\n
                    1: Login
                    0: Return to Main Menu
                 ''')
                staff_choice = get_integer_input("Select an Option: ")
                # Return to main menu
                if staff_choice == 0:
                    break
                # Login page for staff accounts
                elif staff_choice == 1:
                    if login("staff_accounts"):
                        staff_main_menu()
                    break
                else:
                    # Error handling for invald option selected
                    print("Invalid Option")
                    time.sleep(2)
        elif user_choice == 2:
            while True:
                # Print customer portal options
                clear_screen()
                print('''Library Management System\n
                    Welcome to the Customer Portal.\n
                    1: Login
                    2: Register
                    0: Return to Main Menu
                 ''')
                customer_choice = get_integer_input("Select an Option: ")
                # Return to main menu
                if customer_choice == 0:
                    break
                # Login page for customer accounts
                elif customer_choice == 1:
                    if login("customer_accounts"):
                        customer_main_menu()
                    break
                # Register page for new customers
                elif customer_choice == 2:
                    customer_register()
                else:
                    # Error handling for invalid input
                    print("Invalid Option.")
                    time.sleep(2)
        else:
            # Error handling for invalid input
            print("Invalid Option.")
            time.sleep(2)