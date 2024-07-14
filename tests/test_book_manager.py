import unittest
from unittest.mock import patch, MagicMock
from library.managers.book_manager import BookManager
from library.book import Book

class TestBookManager(unittest.TestCase):
    """
    Unit test case for the BookManager class.

    This test case verifies the functionality of the BookManager class,
    ensuring that books can be added, retrieved, updated, deleted, and searched correctly.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes a mock storage object and a BookManager instance.
        It also clears the books list before each test.
        """
        self.mock_storage = MagicMock()
        self.book_manager = BookManager(storage=self.mock_storage)
        self.book_manager.books = []  # Clear books for each test

    def test_add_book(self):
        """
        Test adding a book to the BookManager.

        This test verifies that a book is correctly added to the BookManager
        and that its attributes are set correctly.
        """
        book = self.book_manager.add_book("Test Book", "Test Author", "1234567890")
        self.assertEqual(len(self.book_manager.books), 1)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.isbn, "1234567890")

    def test_add_book_duplicate_isbn(self):
        """
        Test adding a book with a duplicate ISBN.

        This test verifies that adding a book with an ISBN that already exists
        in the BookManager raises a ValueError.
        """
        self.book_manager.add_book("Test Book", "Test Author", "1234567890")
        with self.assertRaises(ValueError):
            self.book_manager.add_book("Another Book", "Another Author", "1234567890")

    def test_get_book_by_isbn(self):
        """
        Test retrieving a book by its ISBN.

        This test verifies that a book can be retrieved from the BookManager
        using its ISBN and that the correct book is returned.
        """
        self.book_manager.add_book("Test Book", "Test Author", "1234567890")
        book = self.book_manager.get_book_by_isbn("1234567890")
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Test Book")

    def test_get_book_by_isbn_not_found(self):
        """
        Test retrieving a book by an ISBN that does not exist.

        This test verifies that attempting to retrieve a book using an ISBN
        that does not exist in the BookManager returns None.
        """
        book = self.book_manager.get_book_by_isbn("9999999999")
        self.assertIsNone(book)

    def test_update_book(self):
        """
        Test updating a book's details.

        This test verifies that a book's title and author can be updated
        and that the changes are correctly saved.
        """
        self.book_manager.add_book("Test Book", "Test Author", "1234567890")
        self.mock_storage.save_data.reset_mock()  # Reset the mock after add_book
        updated_book = self.book_manager.update_book("1234567890", title="Updated Book", author="Updated Author")
        self.assertEqual(updated_book.title, "Updated Book")
        self.assertEqual(updated_book.author, "Updated Author")

    def test_update_book_not_found(self):
        """
        Test updating a book that does not exist.

        This test verifies that attempting to update a book using an ISBN
        that does not exist in the BookManager raises a ValueError.
        """
        with self.assertRaises(ValueError):
            self.book_manager.update_book("9999999999", title="Updated Book")

    def test_delete_book(self):
        """
        Test deleting a book from the BookManager.

        This test verifies that a book can be deleted from the BookManager
        using its ISBN and that it is removed from the books list.
        """
        self.book_manager.add_book("Test Book", "Test Author", "1234567890")
        self.mock_storage.save_data.reset_mock()  # Reset the mock after add_book
        self.book_manager.delete_book("1234567890")
        self.assertEqual(len(self.book_manager.books), 0)

    def test_delete_book_not_found(self):
        """
        Test deleting a book that does not exist.

        This test verifies that attempting to delete a book using an ISBN
        that does not exist in the BookManager raises a ValueError.
        """
        with self.assertRaises(ValueError):
            self.book_manager.delete_book("9999999999")

    def test_search_books(self):
        """
        Test searching for books by title.

        This test verifies that books can be searched by a keyword in their title
        and that the correct books are returned.
        """
        self.book_manager.add_book("Python Programming", "John Doe", "1111111111")
        self.book_manager.add_book("Java Programming", "Jane Smith", "2222222222")
        results = self.book_manager.search_books("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Programming")

if __name__ == '__main__':
    unittest.main()
