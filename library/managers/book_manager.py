from library.book import Book
from library.storage import Storage
import config

class BookManager:
    """
    Manages the collection of books in the library system.

    This class handles operations such as adding, updating, deleting,
    and searching for books, as well as persisting book data.
    """

    def __init__(self, storage=None):
        """
        Initialize the BookManager.

        Args:
            storage (Storage, optional): A Storage instance for persisting data.
                                         If not provided, a new one will be created.
        """
        self.storage = storage or Storage(config.BOOKS_STORAGE_FILE)
        self.books = self._load_books()

    def _load_books(self):
        """
        Load books from storage.

        Returns:
            list: A list of Book objects.
        """
        data = self.storage.load_data()
        return [Book.from_dict(book_data) for book_data in data]

    def save_books(self):
        """Save the current list of books to storage."""
        self.storage.save_data([book.to_dict() for book in self.books])

    def add_book(self, title: str, author: str, isbn: str) -> Book:
        """
        Add a new book to the library.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN of the book.

        Returns:
            Book: The newly added book.

        Raises:
            ValueError: If any required field is missing or if the ISBN already exists.
        """
        if not title or not author or not isbn:
            raise ValueError("Title, author, and ISBN are required.")
        if self.get_book_by_isbn(isbn):
            raise ValueError(f"Book with ISBN {isbn} already exists.")
        book = Book(title, author, isbn)
        self.books.append(book)
        self.save_books()
        return book

    def get_book_by_isbn(self, isbn: str) -> Book:
        """
        Retrieve a book by its ISBN.

        Args:
            isbn (str): The ISBN of the book to retrieve.

        Returns:
            Book: The book with the given ISBN, or None if not found.
        """
        return next((book for book in self.books if book.isbn == isbn), None)

    def list_books(self) -> list:
        """
        Get a list of all books in the library.

        Returns:
            list: A list of all Book objects.
        """
        return self.books

    def update_book(self, isbn: str, title: str = None, author: str = None) -> Book:
        """
        Update a book's information.

        Args:
            isbn (str): The ISBN of the book to update.
            title (str, optional): The new title of the book.
            author (str, optional): The new author of the book.

        Returns:
            Book: The updated book.

        Raises:
            ValueError: If the book with the given ISBN is not found.
        """
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError(f"Book with ISBN {isbn} not found.")
        if title:
            book._title = title
        if author:
            book._author = author
        self.save_books()
        return book

    def delete_book(self, isbn: str):
        """
        Delete a book from the library.

        Args:
            isbn (str): The ISBN of the book to delete.

        Raises:
            ValueError: If the book with the given ISBN is not found.
        """
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError(f"Book with ISBN {isbn} not found.")
        self.books.remove(book)
        self.save_books()

    def search_books(self, keyword: str) -> list:
        """
        Search for books by title or author.

        Args:
            keyword (str): The search keyword.

        Returns:
            list: A list of Book objects that match the search criteria.
        """
        keyword = keyword.lower()
        return [book for book in self.books if keyword in book.title.lower() or keyword in book.author.lower()]