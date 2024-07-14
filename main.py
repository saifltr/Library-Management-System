from library.managers.book_manager import BookManager
from library.managers.user_manager import UserManager
from library.managers.checkout_manager import CheckoutManager
from typing import Optional
import re
from colorama import Fore, Style, init
import os
import sys

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class LibrarySystem:
    def __init__(self):
        self.book_manager = BookManager()
        self.user_manager = UserManager()
        self.checkout_manager = CheckoutManager(self.book_manager, self.user_manager)

    def run(self) -> None:
        while True:
            clear_screen()
            choice = self.main_menu()
            if choice == '1':
                self.manage_books()
            elif choice == '2':
                self.manage_users()
            elif choice == '3':
                clear_screen()
                print(Fore.YELLOW + "Exiting. Goodbye! 👋")
                break
            else:
                print(Fore.RED + "Invalid choice, please try again.")
                input("Press Enter to continue...")

    def main_menu(self) -> str:
        print(Fore.CYAN + "\n📚 Library Management System")
        print("1. 📖 Manage Books")
        print("2. 👥 Manage Users")
        print("3. 🚪 Exit")
        return input(Fore.WHITE + "Enter choice: ")

    def manage_books(self) -> None:
        while True:
            clear_screen()
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

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.update_book()
            elif choice == '3':
                self.delete_book()
            elif choice == '4':
                self.checkout_book()
            elif choice == '5':
                self.return_book()
            elif choice == '6':
                self.list_books()
            elif choice == '7':
                self.search_book()
            elif choice == '8':
                break
            elif choice == '9':
                clear_screen()
                print(Fore.YELLOW + "Exiting. Goodbye! 👋")
                sys.exit()
            else:
                print(Fore.RED + "Invalid choice, please try again.")
            
            input("Press Enter to continue...")

    def manage_users(self) -> None:
        while True:
            clear_screen()
            print(Fore.CYAN + "\n👥 Manage Users")
            print("1. ➕ Add User")
            print("2. 🔄 Update User")
            print("3. 🗑️ Delete User")
            print("4. 📋 List Users")
            print("5. 🔍 Search User")
            print("6. 🔙 Return to Main Menu")
            print("7. 🚪 Exit")
            choice = input(Fore.WHITE + "Enter choice: ")

            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.update_user()
            elif choice == '3':
                self.delete_user()
            elif choice == '4':
                self.list_users()
            elif choice == '5':
                self.search_user()
            elif choice == '6':
                break
            elif choice == '7':
                clear_screen()
                print(Fore.YELLOW + "Exiting. Goodbye! 👋")
                sys.exit()
            else:
                print(Fore.RED + "Invalid choice, please try again.")
            
            input("Press Enter to continue...")

    def add_book(self) -> None:
        clear_screen()
        print(Fore.CYAN + "📕 Add Book")
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
        return bool(re.match(r'^\d{10}$', isbn))

    def update_book(self) -> None:
        clear_screen()
        print(Fore.CYAN + "🔄 Update Book")
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
        clear_screen()
        print(Fore.CYAN + "🗑️ Delete Book")
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
        clear_screen()
        print(Fore.CYAN + "📋 List Books")
        books = self.book_manager.list_books()
        if not books:
            print(Fore.YELLOW + "No books in the library. 📚")
        else:
            for book in books:
                status = "Available ✅" if book.available else "Checked Out ❌"
                print(f"{book} - Status: {status}")
    
    def search_book(self) -> None:
        clear_screen()
        print(Fore.CYAN + "🔍 Search Book")
        print("1. 🔢 Search by ISBN")
        print("2. 📚 Search by Title")
        choice = input(Fore.WHITE + "Enter choice: ")

        if choice == '1':
            isbn = input("Enter ISBN: ")
            if not self.validate_isbn(isbn):
                print(Fore.RED + "Error: ISBN must be a 10-digit number.")
                return
            book = self.book_manager.get_book_by_isbn(isbn)
            if book:
                print(Fore.GREEN + f"Book found: {book}")
            else:
                print(Fore.YELLOW + "No book found with this ISBN.")
        elif choice == '2':
            title = input("Enter title or part of title: ").lower()
            books = self.book_manager.search_books(title)
            if books:
                print(Fore.GREEN + "Books found:")
                for book in books:
                    print(book)
            else:
                print(Fore.YELLOW + "No books found with this title.")
        else:
            print(Fore.RED + "Invalid choice, please try again.")

    def add_user(self) -> None:
        clear_screen()
        print(Fore.CYAN + "➕ Add User")
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
        return bool(re.match(r'^[A-Za-z\s]+$', name))

    def update_user(self) -> None:
        clear_screen()
        print(Fore.CYAN + "🔄 Update User")
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
        clear_screen()
        print(Fore.CYAN + "🗑️ Delete User")
        user_id = input("Enter user ID to delete: ")
        try:
            self.user_manager.delete_user(user_id)
            print(Fore.GREEN + "User deleted successfully. ✅")
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")

    def list_users(self) -> None:
        clear_screen()
        print(Fore.CYAN + "📋 List Users")
        users = self.user_manager.list_users()
        if not users:
            print(Fore.YELLOW + "No users registered. 👥")
        else:
            for user in users:
                print(user)
    
    def search_user(self) -> None:
        clear_screen()
        print(Fore.CYAN + "🔍 Search User")
        print("1. 🆔 Search by ID")
        print("2. 👤 Search by Name")
        choice = input(Fore.WHITE + "Enter choice: ")

        if choice == '1':
            user_id = input("Enter user ID: ")
            user = self.user_manager.get_user_by_id(user_id)
            if user:
                print(Fore.GREEN + f"User found: {user}")
            else:
                print(Fore.YELLOW + "No user found with this ID.")
        elif choice == '2':
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
        else:
            print(Fore.RED + "Invalid choice, please try again.")

    def checkout_book(self) -> None:
        clear_screen()
        print(Fore.CYAN + "📤 Checkout Book")
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
        clear_screen()
        print(Fore.CYAN + "📥 Return Book")
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
    library_system = LibrarySystem()
    library_system.run()

if __name__ == "__main__":
    main()
