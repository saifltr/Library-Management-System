from library.managers.book_manager import BookManager
from library.managers.user_manager import UserManager
from library.managers.checkout_manager import CheckoutManager
from typing import Optional
import re
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)

class LibrarySystem:
    """
    Main class for the Library Management System.
    
    This class orchestrates the interaction between users and the system,
    managing books, users, and checkouts through a command-line interface.
    """

    def __init__(self):
        """
        Initialize the LibrarySystem with its core components.
        """
        self.book_manager = BookManager()
        self.user_manager = UserManager()
        self.checkout_manager = CheckoutManager(self.book_manager, self.user_manager)

    def run(self) -> None:
        """
        Start the main loop of the Library Management System.
        
        This method displays the main menu and handles user input until the user chooses to exit.
        """
        while True:
            choice = self.main_menu()
            if choice == '1':
                self.manage_books()
            elif choice == '2':
                self.manage_users()
            elif choice == '3':
                print(Fore.YELLOW + "Exiting. Goodbye! 👋")
                break
            else:
                print(Fore.RED + "Invalid choice, please try again.")

    def main_menu(self) -> str:
        """
        Display the main menu and get user choice.

        Returns:
            str: The user's menu choice.
        """
        print(Fore.CYAN + "\n📚 Library Management System")
        print("1. 📖 Manage Books")
        print("2. 👥 Manage Users")
        print("3. 🚪 Exit")
        return input(Fore.WHITE + "Enter choice: ")

    def manage_books(self) -> None:
        """
        Handle the book management submenu and associated operations.
        """
        while True:
            print(Fore.CYAN + "\n📖 Manage Books")
            print("1. 📕 Add Book")
            print("2. 🔄 Update Book")
            print("3. 🗑️ Delete Book")
            print("4. 📤 Checkout Book")
            print("5. 📥 Return Book")
            print("6. 📋 List Books")
            print("7. 🔍 Search Book")
            print("8. 🔙 Return to Main Menu")
            print("9. 🚪 Exit")
            choice = input(Fore.WHITE + "Enter choice: ")

            # Dictionary to map choices to methods
            actions = {
                '1': self.add_book,
                '2': self.update_book,
                '3': self.delete_book,
                '4': self.checkout_book,
                '5': self.return_book,
                '6': self.list_books,
                '7': self.search_book
            }

            if choice in actions:
                actions[choice]()
            elif choice == '8':
                break
            elif choice == '9':
                print(Fore.YELLOW + "Exiting. Goodbye! 👋")
                exit()
            else:
                print(Fore.RED + "Invalid choice, please try again.")

    def manage_users(self) -> None:
        """
        Handle the user management submenu and associated operations.
        """
        while True:
            print(Fore.CYAN + "\n👥 Manage Users")
            print("1. ➕ Add User")
            print("2. 🔄 Update User")
            print("3. 🗑️ Delete User")
            print("4. 📋 List Users")
            print("5. 🔍 Search User")
            print("6. 🔙 Return to Main Menu")
            print("7. 🚪 Exit")
            choice = input(Fore.WHITE + "Enter choice: ")

            # Dictionary to map choices to methods
            actions = {
                '1': self.add_user,
                '2': self.update_user,
                '3': self.delete_user,
                '4': self.list_users,
                '5': self.search_user
            }

            if choice in actions:
                actions[choice]()
            elif choice == '6':
                break
            elif choice == '7':
                print(Fore.YELLOW + "Exiting. Goodbye! 👋")
                exit()
            else:
                print(Fore.RED + "Invalid choice, please try again.")

    def add_book(self) -> None:
        """
        Add a new book to the library system.
        
        This method handles user input, validates the data, and adds the book to the system.
        """
        title = input("Enter title: ")
        author = input("Enter author: ")
        isbn = input("Enter ISBN (10 digits): ")
        
        if not self.validate_isbn(isbn):
            print(Fore.RED + "Error: ISBN must be a 10-digit number.")
            return
        
        if not self.validate_name(author):
            print(Fore.RED + "Error: Author Name must contain only letters and spaces.")
            return
        
        try:
            book = self.book_manager.add_book(title, author, isbn)
            print(Fore.GREEN + f"Book added: {book} ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

    def validate_isbn(self, isbn: str) -> bool:
        """
        Validate the ISBN format.

        Args:
            isbn (str): The ISBN to validate.

        Returns:
            bool: True if the ISBN is valid, False otherwise.
        """
        return bool(re.match(r'^\d{10}$', isbn))

    def update_book(self) -> None:
        """
        Update an existing book's information.
        
        This method handles user input, validates the data, and updates the book in the system.
        """
        isbn = input("Enter ISBN of the book to update: ")
        if not self.validate_isbn(isbn):
            print(Fore.RED + "Error: ISBN must be a 10-digit number.")
            return

        title = input("Enter new title (press enter to keep current): ")
        author = input("Enter new author (press enter to keep current): ")
        
        if author and not self.validate_name(author):
            print(Fore.RED + "Error: Author Name must contain only letters and spaces.")
            return

        try:
            book = self.book_manager.update_book(isbn, title if title else None, author if author else None)
            print(Fore.GREEN + f"Book updated: {book} ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

    def delete_book(self) -> None:
        """
        Delete a book from the library system.
        
        This method handles user input, validates the ISBN, and removes the book from the system.
        """
        isbn = input("Enter ISBN of the book to delete: ")
        if not self.validate_isbn(isbn):
            print(Fore.RED + "Error: ISBN must be a 10-digit number.")
            return

        try:
            self.book_manager.delete_book(isbn)
            print(Fore.GREEN + "Book deleted successfully. ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

    def list_books(self) -> None:
        """
        Display a list of all books in the library system.
        """
        books = self.book_manager.list_books()
        if not books:
            print(Fore.YELLOW + "No books in the library. 📚")
        else:
            for book in books:
                status = "Available ✅" if book.available else "Checked Out ❌"
                print(f"{book} - Status: {status}")
    
    def search_book(self) -> None:
        """
        Search for books by ISBN or title.
        
        This method provides a submenu for choosing the search type and handles the search process.
        """
        print(Fore.CYAN + "\n🔍 Search Book")
        print("1. 🔢 Search by ISBN")
        print("2. 📚 Search by Title")
        choice = input(Fore.WHITE + "Enter choice: ")

        if choice == '1':
            self._search_book_by_isbn()
        elif choice == '2':
            self._search_book_by_title()
        else:
            print(Fore.RED + "Invalid choice, please try again.")

    def _search_book_by_isbn(self) -> None:
        """
        Helper method to search for a book by ISBN.
        """
        isbn = input("Enter ISBN: ")
        if not self.validate_isbn(isbn):
            print(Fore.RED + "Error: ISBN must be a 10-digit number.")
            return
        book = self.book_manager.get_book_by_isbn(isbn)
        if book:
            print(Fore.GREEN + f"Book found: {book}")
        else:
            print(Fore.YELLOW + "No book found with this ISBN.")

    def _search_book_by_title(self) -> None:
        """
        Helper method to search for books by title.
        """
        title = input("Enter title or part of title: ").lower()
        books = self.book_manager.search_books(title)
        if books:
            print(Fore.GREEN + "Books found:")
            for book in books:
                print(book)
        else:
            print(Fore.YELLOW + "No books found with this title.")

    def add_user(self) -> None:
        """
        Add a new user to the library system.
        
        This method handles user input, validates the name, and adds the user to the system.
        """
        name = input("Enter user name: ")
        if not self.validate_name(name):
            print(Fore.RED + "Error: Name must contain only letters and spaces.")
            return

        try:
            user = self.user_manager.add_user(name)
            print(Fore.GREEN + f"User added: {user} ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

    def validate_name(self, name: str) -> bool:
        """
        Validate the format of a name.

        Args:
            name (str): The name to validate.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        return bool(re.match(r'^[A-Za-z\s]+$', name))

    def update_user(self) -> None:
        """
        Update an existing user's information.
        
        This method handles user input, validates the data, and updates the user in the system.
        """
        user_id = input("Enter user ID to update: ")
        name = input("Enter new name: ")
        if not self.validate_name(name):
            print(Fore.RED + "Error: Name must contain only letters and spaces.")
            return

        try:
            user = self.user_manager.update_user(user_id, name)
            print(Fore.GREEN + f"User updated: {user} ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

    def delete_user(self) -> None:
        """
        Delete a user from the library system.
        
        This method handles user input and removes the user from the system.
        """
        user_id = input("Enter user ID to delete: ")
        try:
            self.user_manager.delete_user(user_id)
            print(Fore.GREEN + "User deleted successfully. ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

    def list_users(self) -> None:
        """
        Display a list of all users in the library system.
        """
        users = self.user_manager.list_users()
        if not users:
            print(Fore.YELLOW + "No users registered. 👥")
        else:
            for user in users:
                print(user)
    
    def search_user(self) -> None:
        """
        Search for users by ID or name.
        
        This method provides a submenu for choosing the search type and handles the search process.
        """
        print(Fore.CYAN + "\n🔍 Search User")
        print("1. 🆔 Search by ID")
        print("2. 👤 Search by Name")
        choice = input(Fore.WHITE + "Enter choice: ")

        if choice == '1':
            self._search_user_by_id()
        elif choice == '2':
            self._search_user_by_name()
        else:
            print(Fore.RED + "Invalid choice, please try again.")

    def _search_user_by_id(self) -> None:
        """
        Helper method to search for a user by ID.
        """
        user_id = input("Enter user ID: ")
        user = self.user_manager.get_user_by_id(user_id)
        if user:
            print(Fore.GREEN + f"User found: {user}")
        else:
            print(Fore.YELLOW + "No user found with this ID.")

    def _search_user_by_name(self) -> None:
        """
        Helper method to search for users by name.
        """
        name = input("Enter user name or part of name: ")
        if not self.validate_name(name):
            print(Fore.RED + "Error: Name must contain only letters and spaces.")
            return
        users = self.user_manager.search_users(name)
        if users:
            print(Fore.GREEN + "Users found:")
            for user in users:
                print(user)
        else:
            print(Fore.YELLOW + "No users found with this name.")

    def checkout_book(self) -> None:
        """
        Handle the process of checking out a book to a user.
        
        This method handles user input, validates the data, and processes the checkout.
        """
        user_id = input("Enter user ID: ")
        isbn = input("Enter ISBN of the book to checkout: ")
        if not self.validate_isbn(isbn):
            print(Fore.RED + "Error: ISBN must be a 10-digit number.")
            return

        try:
            checkout = self.checkout_manager.checkout_book(user_id, isbn)
            print(Fore.GREEN + f"Book checked out: {checkout} ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

    def return_book(self) -> None:
        """
        Handle the process of returning a book to the library.
        
        This method handles user input, validates the ISBN, and processes the return.
        """
        isbn = input("Enter ISBN of the book to return: ")
        if not self.validate_isbn(isbn):
            print(Fore.RED + "Error: ISBN must be a 10-digit number.")
            return

        try:
            self.checkout_manager.return_book(isbn)
            print(Fore.GREEN + "Book returned successfully. ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

def main() -> None:
    """
    Main entry point of the Library Management System.
    
    This function creates an instance of LibrarySystem and starts its main loop.
    """
    library_system = LibrarySystem()
    library_system.run()

if __name__ == "__main__":
    main()