import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                BookID TEXT PRIMARY KEY,
                Title TEXT,
                Author TEXT,
                ISBN TEXT,
                Status TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                UserID TEXT PRIMARY KEY,
                Name TEXT,
                Email TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reservations (
                ReservationID TEXT PRIMARY KEY,
                BookID TEXT,
                UserID TEXT,
                ReservationDate TEXT,
                FOREIGN KEY (BookID) REFERENCES Books(BookID),
                FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )
        ''')

        self.conn.commit()

    def close(self):
        self.conn.close()

class BookManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.conn = self.db_manager.conn
        self.cursor = self.db_manager.cursor

    def add_book(self):
        book_id = input("Enter BookID: ")
        self.cursor.execute("SELECT BookID FROM Books WHERE BookID = ?", (book_id,))
        existing_book = self.cursor.fetchone()

        if existing_book:
            print(f"Book with BookID {book_id} already exists.")
            return

        title = input("Enter Title: ")
        author = input("Enter Author: ")
        isbn = input("Enter ISBN: ")
        status = "Available"

        self.cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
                            (book_id, title, author, isbn, status))
        self.conn.commit()
        print("Book added successfully!")

    def find_book_details(self):
        book_id = input("Enter BookID: ")
        self.cursor.execute('''
            SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                   Reservations.ReservationID, Users.UserID, Users.Name, Users.Email, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = ?''', (book_id,))

        results = self.cursor.fetchall()
        headers = ["BookID", "Title", "Author", "ISBN", "Status", "ReservationID", "UserID", "Name", "Email", "ReservationDate"]

        self.print_query_results(results, headers)

    def find_reservation_status(self):
        search_term = input("Enter BookID, UserID, Title, or ReservationID: ")

        if search_term.startswith("LB"):
            # Query reservation status for a book based on BookID
            self.cursor.execute('''
                SELECT Books.BookID, Books.Title, Books.Status,
                    Reservations.ReservationID, Users.UserID, Users.Name, Users.Email, Reservations.ReservationDate
                FROM Books
                LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                LEFT JOIN Users ON Reservations.UserID = Users.UserID
                WHERE Books.BookID = ?''', (search_term,))
        elif search_term.startswith("LU"):
            # Query reservation status for a user based on UserID
            self.cursor.execute('''
                SELECT Books.BookID, Books.Title, Books.Status,
                    Reservations.ReservationID, Users.UserID, Users.Name, Users.Email, Reservations.ReservationDate
                FROM Books
                LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                LEFT JOIN Users ON Reservations.UserID = Users.UserID
                WHERE Users.UserID = ?''', (search_term,))
        elif search_term.startswith("LR"):
            # Query reservation status for a book based on ReservationID
            self.cursor.execute('''
                SELECT Books.BookID, Books.Title, Books.Status,
                    Reservations.ReservationID, Users.UserID, Users.Name, Users.Email, Reservations.ReservationDate
                FROM Books
                LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                LEFT JOIN Users ON Reservations.UserID = Users.UserID
                WHERE Reservations.ReservationID = ?''', (search_term,))
        else:
            # Query reservation status for a book based on Title
            self.cursor.execute('''
                SELECT Books.BookID, Books.Title, Books.Status,
                    Reservations.ReservationID, Users.UserID, Users.Name, Users.Email, Reservations.ReservationDate
                FROM Books
                LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                LEFT JOIN Users ON Reservations.UserID = Users.UserID
                WHERE Books.Title = ?''', (search_term,))

        results = self.cursor.fetchall()
        headers = ["BookID", "Title", "Status", "ReservationID", "UserID", "Name", "Email", "ReservationDate"]

        print("Search results:")
        self.print_query_results(results, headers)

    def find_all_books(self):
        self.cursor.execute('''
            SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                   Reservations.ReservationID, Users.UserID, Users.Name, Users.Email, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
        ''')

        results = self.cursor.fetchall()
        headers = ["BookID", "Title", "Author", "ISBN", "Status", "ReservationID", "UserID", "Name", "Email", "ReservationDate"]

        self.print_query_results(results, headers)

    def update_book_details(self):
        book_id = input("Enter the BookID to update details: ")
        status = input("Enter the new status (Available/Reserved): ")

        self.cursor.execute("SELECT Status FROM Books WHERE BookID = ?", (book_id,))
        current_status = self.cursor.fetchone()

        if current_status is None:
            print(f"Book with BookID {book_id} does not exist.")
            return

        # Check if the modification involves updating the reservation status
        if current_status[0] != status:
            self.cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (status, book_id))
            self.conn.commit()

            if status == "Available":
                # If the new status is "Available", remove reservations
                self.cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
                self.conn.commit()
                print(f"Book with BookID {book_id} is now available and all reservations have been removed.")
            elif status == "Reserved":
                # If the new status is "Reserved", update reservations
                reservation_date = input("Enter the new Reservation Date (YYYY-MM-DD): ")
                self.cursor.execute("UPDATE Reservations SET ReservationDate = ? WHERE BookID = ?", (reservation_date, book_id))
                self.conn.commit()
                print(f"Book with BookID {book_id} is now reserved.")
        else:
            print(f"Book with BookID {book_id} status remains the same: {status}")

    def delete_book(self):
        book_id = input("Enter the BookID to delete: ")

        self.cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        self.cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        self.conn.commit()

        print("Book deleted successfully!")

    def print_query_results(self, results, headers):
        if results:
            for result in results:
                record = {headers[i]: result[i] for i in range(len(headers))}
                print("Record Details:")
                for key, value in record.items():
                    print(f"{key}: {value}")
                print()
        else:
            print("No results found.")

class Menu:
    def __init__(self, book_manager):
        self.book_manager = book_manager

    def display_menu(self):
        print("\nLibrary Management System Menu:")
        print("1. Add a new book to the database")
        print("2. Find book details by BookID")
        print("3. Find reservation status")
        print("4. Find all books")
        print("5. Update book details")
        print("6. Delete book by BookID")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            self.book_manager.add_book()
        elif choice == '2':
            self.book_manager.find_book_details()
        elif choice == '3':
            self.book_manager.find_reservation_status()
        elif choice == '4':
            self.book_manager.find_all_books()
        elif choice == '5':
            self.book_manager.update_book_details()
        elif choice == '6':
            self.book_manager.delete_book()
        elif choice == '7':
            print("Exiting the program. Goodbye!")
            self.book_manager.db_manager.close()
            exit()
        else:
            print("Invalid choice. Please try again.")

def main():
    # Database file path
    db_path = os.path.join("Exercise_4", "library.db")

    # Check if the database file exists
    if not os.path.exists(db_path):
        print("Database does not exist. Creating a new one.")
        db_manager = DatabaseManager(db_path)
        db_manager.connect()
        db_manager.create_tables()
    else:
        response = input("Database already exists. Do you want to clear it and start fresh? (yes/no): ")
        if response.lower() == "yes":
            os.remove(db_path)
            print("Database cleared.")
            db_manager = DatabaseManager(db_path)
            db_manager.connect()
            db_manager.create_tables()
        else:
            db_manager = DatabaseManager(db_path)
            db_manager.connect()

    # Create a book manager object
    book_manager = BookManager(db_manager)

    # Create a menu object
    menu = Menu(book_manager)

    while True:
        # Display the menu and handle user input
        menu.display_menu()

if __name__ == "__main__":
    main()