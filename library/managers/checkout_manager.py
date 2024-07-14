from library.checkout import Checkout
from library.storage import Storage
from library.managers.book_manager import BookManager
from library.managers.user_manager import UserManager
import config

class CheckoutManager:
    """
    Manages the checkout process in the library system.

    This class handles operations such as checking out books, returning books,
    and keeping track of all checkouts.
    """

    def __init__(self, book_manager: BookManager, user_manager: UserManager):
        """
        Initialize the CheckoutManager.

        Args:
            book_manager (BookManager): The BookManager instance to use.
            user_manager (UserManager): The UserManager instance to use.
        """
        self.storage = Storage(config.CHECKOUTS_STORAGE_FILE)
        self.book_manager = book_manager
        self.user_manager = user_manager
        self.checkouts = self._load_checkouts()

    def _load_checkouts(self) -> list:
        """
        Load checkouts from storage.

        Returns:
            list: A list of valid Checkout objects.
        """
        data = self.storage.load_data()
        checkouts = []
        for checkout_data in data:
            try:
                checkout = Checkout.from_dict(checkout_data, self.user_manager, self.book_manager)
                if checkout.user and checkout.book:
                    checkouts.append(checkout)
            except AttributeError:
                # Skip invalid checkouts
                pass
        return checkouts

    def save_checkouts(self):
        """Save the current list of checkouts to storage."""
        valid_checkouts = [checkout for checkout in self.checkouts if checkout.user and checkout.book]
        self.storage.save_data([checkout.to_dict() for checkout in valid_checkouts])

    def checkout_book(self, user_id: str, isbn: str) -> Checkout:
        """
        Check out a book to a user.

        Args:
            user_id (str): The ID of the user checking out the book.
            isbn (str): The ISBN of the book being checked out.

        Returns:
            Checkout: The newly created Checkout object.

        Raises:
            ValueError: If the user or book is not found, or if the book is not available.
        """
        user = self.user_manager.get_user_by_id(user_id)
        book = self.book_manager.get_book_by_isbn(isbn)
        
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        if not book:
            raise ValueError(f"Book with ISBN {isbn} not found")
        
        if not book.available:
            raise ValueError("Book is not available for checkout")
        
        checkout = Checkout(user, book)
        book.available = False
        self.checkouts.append(checkout)
        self.save_checkouts()
        self.book_manager.save_books()
        return checkout

    def return_book(self, isbn: str):
        """
        Return a checked-out book.

        Args:
            isbn (str): The ISBN of the book being returned.

        Raises:
            ValueError: If the book is not found or has already been returned.
        """
        checkout = next((c for c in self.checkouts if c.book and c.book.isbn == isbn and not c.book.available), None)
        if not checkout:
            raise ValueError("Book not found or already returned")
        
        if not checkout.book:
            raise ValueError("Invalid checkout: book information is missing")
        
        checkout.book.available = True
        self.checkouts.remove(checkout)
        self.save_checkouts()
        self.book_manager.save_books()

    def get_checked_out_books(self) -> list:
        """
        Get a list of all currently checked-out books.

        Returns:
            list: A list of Book objects that are currently checked out.
        """
        return [checkout.book for checkout in self.checkouts if checkout.book and not checkout.book.available]