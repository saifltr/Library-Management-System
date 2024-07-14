from abc import ABC, abstractmethod

class LibraryItem(ABC):
    """
    Abstract base class for library items.

    This class defines the common attributes and methods for all library items.
    It uses the ABC module to create an abstract base class, ensuring that
    child classes implement certain methods.
    """

    def __init__(self, title: str, isbn: str):
        """
        Initialize a LibraryItem.

        Args:
            title (str): The title of the library item.
            isbn (str): ISBN of the item.
        """
        self._title = title
        self._isbn = isbn
        self._available = True  # Items are available by default when created

    @property
    def title(self) -> str:
        """Get the title of the library item."""
        return self._title

    @property
    def isbn(self) -> str:
        """Get the ISBN of the library item."""
        return self._isbn

    @property
    def available(self) -> bool:
        """Check if the library item is available for checkout."""
        return self._available

    @available.setter
    def available(self, value: bool):
        """Set the availability status of the library item."""
        self._available = value

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the library item.

        This method must be implemented by all subclasses.
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Convert the library item to a dictionary.

        This method must be implemented by all subclasses and is used for serialization.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """
        Create a library item from a dictionary.

        This class method must be implemented by all subclasses and is used for deserialization.

        Args:
            data (dict): A dictionary containing the library item's data.
        """
        pass

class Book(LibraryItem):
    """
    Represents a book in the library system.

    This class inherits from LibraryItem and implements its abstract methods.
    """

    def __init__(self, title: str, author: str, isbn: str):
        """
        Initialize a Book.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN of the book.
        """
        super().__init__(title, isbn)
        self._author = author

    @property
    def author(self) -> str:
        """Get the author of the book."""
        return self._author

    def __str__(self) -> str:
        """
        Return a string representation of the book.

        Returns:
            str: A string containing the book's title, author, and ISBN.
        """
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def to_dict(self) -> dict:
        """
        Convert the book to a dictionary.

        Returns:
            dict: A dictionary containing the book's data.
        """
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Book instance from a dictionary.

        Args:
            data (dict): A dictionary containing the book's data.

        Returns:
            Book: A new Book instance created from the provided data.
        """
        book = cls(data["title"], data["author"], data["isbn"])
        book.available = data["available"]
        return book