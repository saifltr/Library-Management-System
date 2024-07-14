import unittest
from unittest.mock import patch, MagicMock
from library.managers.checkout_manager import CheckoutManager
from library.managers.book_manager import BookManager
from library.managers.user_manager import UserManager
from library.book import Book
from library.user import User
from library.checkout import Checkout
from datetime import datetime, timedelta

class TestCheckoutManager(unittest.TestCase):
    """
    Unit test case for the CheckoutManager class.

    This test case verifies the functionality of the CheckoutManager class,
    ensuring that books can be checked out, returned, and managed correctly.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes mock objects for storage, book manager, and user manager,
        and creates an instance of CheckoutManager with these mocks. It also clears the
        checkouts list before each test.
        """
        self.mock_storage = MagicMock()
        self.mock_book_manager = MagicMock(spec=BookManager)
        self.mock_user_manager = MagicMock(spec=UserManager)
        self.checkout_manager = CheckoutManager(self.mock_book_manager, self.mock_user_manager)
        self.checkout_manager.storage = self.mock_storage
        self.checkout_manager.checkouts = []  # Clear checkouts for each test

    def test_checkout_book(self):
        """
        Test checking out a book.

        This test verifies that a book can be checked out by a user, the checkout is
        recorded, and the book's availability status is updated.
        """
        mock_user = User("Test User", "1")
        mock_book = Book("Test Book", "Test Author", "1234567890")
        mock_book.available = True
        
        self.mock_user_manager.get_user_by_id.return_value = mock_user
        self.mock_book_manager.get_book_by_isbn.return_value = mock_book

        checkout = self.checkout_manager.checkout_book("1", "1234567890")
        
        self.assertEqual(len(self.checkout_manager.checkouts), 1)
        self.assertEqual(checkout.user, mock_user)
        self.assertEqual(checkout.book, mock_book)
        self.assertFalse(mock_book.available)

    def test_checkout_book_user_not_found(self):
        """
        Test checking out a book with a non-existent user.

        This test verifies that attempting to check out a book with a user ID that
        does not exist in the user manager raises a ValueError.
        """
        self.mock_user_manager.get_user_by_id.return_value = None
        
        with self.assertRaises(ValueError):
            self.checkout_manager.checkout_book("999", "1234567890")

    def test_checkout_book_book_not_found(self):
        """
        Test checking out a non-existent book.

        This test verifies that attempting to check out a book with an ISBN that
        does not exist in the book manager raises a ValueError.
        """
        mock_user = User("Test User", "1")
        self.mock_user_manager.get_user_by_id.return_value = mock_user
        self.mock_book_manager.get_book_by_isbn.return_value = None
        
        with self.assertRaises(ValueError):
            self.checkout_manager.checkout_book("1", "9999999999")

    def test_checkout_book_not_available(self):
        """
        Test checking out a book that is not available.

        This test verifies that attempting to check out a book that is already
        checked out (not available) raises a ValueError.
        """
        mock_user = User("Test User", "1")
        mock_book = Book("Test Book", "Test Author", "1234567890")
        mock_book.available = False
        
        self.mock_user_manager.get_user_by_id.return_value = mock_user
        self.mock_book_manager.get_book_by_isbn.return_value = mock_book
        
        with self.assertRaises(ValueError):
            self.checkout_manager.checkout_book("1", "1234567890")

    def test_return_book(self):
        """
        Test returning a book.

        This test verifies that a book can be returned, the checkout record is
        removed, and the book's availability status is updated.
        """
        mock_user = User("Test User", "1")
        mock_book = Book("Test Book", "Test Author", "1234567890")
        mock_book.available = False
        checkout = Checkout(mock_user, mock_book)
        self.checkout_manager.checkouts.append(checkout)

        self.checkout_manager.return_book("1234567890")
        
        self.assertEqual(len(self.checkout_manager.checkouts), 0)
        self.assertTrue(mock_book.available)

    def test_return_book_not_found(self):
        """
        Test returning a non-existent book.

        This test verifies that attempting to return a book with an ISBN that
        does not have a corresponding checkout record raises a ValueError.
        """
        with self.assertRaises(ValueError):
            self.checkout_manager.return_book("9999999999")

    def test_get_checked_out_books(self):
        """
        Test getting all checked-out books.

        This test verifies that all currently checked-out books can be retrieved
        and that the correct books are returned.
        """
        mock_user = User("Test User", "1")
        mock_book1 = Book("Test Book 1", "Test Author 1", "1111111111")
        mock_book2 = Book("Test Book 2", "Test Author 2", "2222222222")
        mock_book1.available = False
        mock_book2.available = False
        
        self.checkout_manager.checkouts = [
            Checkout(mock_user, mock_book1),
            Checkout(mock_user, mock_book2)
        ]

        checked_out_books = self.checkout_manager.get_checked_out_books()
        
        self.assertEqual(len(checked_out_books), 2)
        self.assertIn(mock_book1, checked_out_books)
        self.assertIn(mock_book2, checked_out_books)

    def test_load_checkouts(self):
        """
        Test loading checkouts from storage.

        This test verifies that checkout records can be loaded from storage,
        and the corresponding user and book objects are correctly instantiated.
        """
        mock_checkout_data = [
            {
                "user_id": "1",
                "book_isbn": "1234567890",
                "checkout_date": datetime.now().isoformat(),
                "due_date": (datetime.now() + timedelta(days=14)).isoformat()
            }
        ]
        self.mock_storage.load_data.return_value = mock_checkout_data
        
        mock_user = User("Test User", "1")
        mock_book = Book("Test Book", "Test Author", "1234567890")
        self.mock_user_manager.get_user_by_id.return_value = mock_user
        self.mock_book_manager.get_book_by_isbn.return_value = mock_book

        # Patch the _load_checkouts method to use our mocked data
        with patch.object(CheckoutManager, '_load_checkouts', return_value=[Checkout(mock_user, mock_book)]):
            checkout_manager = CheckoutManager(self.mock_book_manager, self.mock_user_manager)
            checkout_manager.storage = self.mock_storage

            self.assertEqual(len(checkout_manager.checkouts), 1)
            loaded_checkout = checkout_manager.checkouts[0]
            self.assertEqual(loaded_checkout.user, mock_user)
            self.assertEqual(loaded_checkout.book, mock_book)

if __name__ == '__main__':
    unittest.main()
