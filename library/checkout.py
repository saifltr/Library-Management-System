from datetime import datetime, timedelta

class Checkout:
    """
    Represents a checkout transaction in the library system.

    This class manages the details of a book checkout, including the user who checked out the book,
    the book itself, and the relevant dates.
    """

    def __init__(self, user, book):
        """
        Initialize a Checkout.

        Args:
            user: The User who is checking out the book.
            book: The Book being checked out.
        """
        self.user = user
        self.book = book
        self.checkout_date = datetime.now()
        self.due_date = self.checkout_date + timedelta(days=14)  # 2 weeks checkout period

    def __str__(self) -> str:
        """
        Return a string representation of the checkout.

        Returns:
            str: A string containing the book title, user name, and due date.
        """
        user_name = self.user.name if self.user else "Unknown User"
        book_title = self.book.title if self.book else "Unknown Book"
        return f"{book_title} checked out by {user_name} until {self.due_date.strftime('%Y-%m-%d')}"

    def to_dict(self) -> dict:
        """
        Convert the checkout to a dictionary.

        Returns:
            dict: A dictionary containing the checkout's data.
        """
        return {
            "user_id": self.user.user_id if self.user else None,
            "book_isbn": self.book.isbn if self.book else None,
            "checkout_date": self.checkout_date.isoformat(),
            "due_date": self.due_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict, user_manager, book_manager):
        """
        Create a Checkout instance from a dictionary.

        Args:
            data (dict): A dictionary containing the checkout's data.
            user_manager: The UserManager instance to retrieve the user.
            book_manager: The BookManager instance to retrieve the book.

        Returns:
            Checkout: A new Checkout instance created from the provided data.
        """
        user = user_manager.get_user_by_id(data["user_id"]) if data["user_id"] else None
        book = book_manager.get_book_by_isbn(data["book_isbn"]) if data["book_isbn"] else None
        checkout = cls(user, book)
        checkout.checkout_date = datetime.fromisoformat(data["checkout_date"])
        checkout.due_date = datetime.fromisoformat(data["due_date"])
        return checkout