import unittest
from unittest.mock import patch, MagicMock, call
from io import StringIO
from library.managers.book_manager import BookManager
from library.managers.user_manager import UserManager
from library.managers.checkout_manager import CheckoutManager
from main import LibrarySystem

class TestLibrarySystem(unittest.TestCase):
    """
    Unit test case for the LibrarySystem class.

    This test case verifies the functionality of the LibrarySystem class,
    ensuring that book and user management, as well as checkouts, are handled correctly.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes mock objects for book manager, user manager, and checkout manager,
        and creates an instance of LibrarySystem with these mocks.
        """
        self.book_manager = MagicMock(spec=BookManager)
        self.user_manager = MagicMock(spec=UserManager)
        self.checkout_manager = MagicMock(spec=CheckoutManager)
        
        # Create a LibrarySystem instance with mocked managers
        self.library_system = LibrarySystem()
        self.library_system.book_manager = self.book_manager
        self.library_system.user_manager = self.user_manager
        self.library_system.checkout_manager = self.checkout_manager

    @patch('builtins.input', side_effect=['1', '8', '3'])
    def test_run_manage_books(self, mock_input):
        """
        Test running the library system with a sequence of inputs to manage books.

        This test verifies that the library system can handle book management and exit correctly.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library_system.run()
            self.assertIn("Exiting. Goodbye!", fake_out.getvalue())

    @patch('builtins.input', side_effect=['2', '6', '3'])
    def test_run_manage_users(self, mock_input):
        """
        Test running the library system with a sequence of inputs to manage users.

        This test verifies that the library system can handle user management and exit correctly.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library_system.run()
            self.assertIn("Exiting. Goodbye!", fake_out.getvalue())

    @patch('builtins.input', side_effect=['4', '3'])
    def test_run_invalid_choice(self, mock_input):
        """
        Test running the library system with an invalid menu choice.

        This test verifies that the library system handles invalid menu choices by prompting the user again.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library_system.run()
            self.assertIn("Invalid choice, please try again.", fake_out.getvalue())

    @patch('builtins.input', side_effect=['Test Book', 'Test Author', '1234567890'])
    def test_add_book(self, mock_input):
        """
        Test adding a book to the library system.

        This test verifies that a book can be added correctly by calling the book manager's add_book method.
        """
        self.book_manager.add_book.return_value = MagicMock()
        self.library_system.add_book()
        self.book_manager.add_book.assert_called_once_with('Test Book', 'Test Author', '1234567890')

    @patch('builtins.input', side_effect=['1234567890', 'New Title', 'New Author'])
    def test_update_book(self, mock_input):
        """
        Test updating a book in the library system.

        This test verifies that a book's information can be updated correctly by calling the book manager's update_book method.
        """
        self.book_manager.update_book.return_value = MagicMock()
        self.library_system.update_book()
        self.book_manager.update_book.assert_called_once_with('1234567890', 'New Title', 'New Author')

    @patch('builtins.input', return_value='1234567890')
    def test_delete_book(self, mock_input):
        """
        Test deleting a book from the library system.

        This test verifies that a book can be deleted correctly by calling the book manager's delete_book method.
        """
        self.library_system.delete_book()
        self.book_manager.delete_book.assert_called_once_with('1234567890')

    def test_list_books(self):
        """
        Test listing all books in the library system.

        This test verifies that the list of books is correctly retrieved and displayed, showing their availability status.
        """
        mock_book1 = MagicMock()
        mock_book1.__str__.return_value = "Book 1"
        mock_book1.available = True
        mock_book2 = MagicMock()
        mock_book2.__str__.return_value = "Book 2"
        mock_book2.available = False
        self.book_manager.list_books.return_value = [mock_book1, mock_book2]
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library_system.list_books()
            self.assertIn("Book 1 - Status: Available ✅", fake_out.getvalue())
            self.assertIn("Book 2 - Status: Checked Out ❌", fake_out.getvalue())

    @patch('builtins.input', side_effect=['Test User'])
    def test_add_user(self, mock_input):
        """
        Test adding a user to the library system.

        This test verifies that a user can be added correctly by calling the user manager's add_user method.
        """
        self.user_manager.add_user.return_value = MagicMock()
        self.library_system.add_user()
        self.user_manager.add_user.assert_called_once_with('Test User')

    @patch('builtins.input', side_effect=['1', 'New Name'])
    def test_update_user(self, mock_input):
        """
        Test updating a user in the library system.

        This test verifies that a user's information can be updated correctly by calling the user manager's update_user method.
        """
        self.user_manager.update_user.return_value = MagicMock()
        self.library_system.update_user()
        self.user_manager.update_user.assert_called_once_with('1', 'New Name')

    @patch('builtins.input', return_value='1')
    def test_delete_user(self, mock_input):
        """
        Test deleting a user from the library system.

        This test verifies that a user can be deleted correctly by calling the user manager's delete_user method.
        """
        self.library_system.delete_user()
        self.user_manager.delete_user.assert_called_once_with('1')

    def test_list_users(self):
        """
        Test listing all users in the library system.

        This test verifies that the list of users is correctly retrieved and displayed.
        """
        mock_user1 = MagicMock()
        mock_user1.__str__.return_value = "User 1"
        mock_user2 = MagicMock()
        mock_user2.__str__.return_value = "User 2"
        self.user_manager.list_users.return_value = [mock_user1, mock_user2]
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library_system.list_users()
            self.assertIn("User 1", fake_out.getvalue())
            self.assertIn("User 2", fake_out.getvalue())

    @patch('builtins.input', side_effect=['1', '1234567890'])
    def test_checkout_book(self, mock_input):
        """
        Test checking out a book from the library system.

        This test verifies that a book can be checked out correctly by calling the checkout manager's checkout_book method.
        """
        self.checkout_manager.checkout_book.return_value = MagicMock()
        self.library_system.checkout_book()
        self.checkout_manager.checkout_book.assert_called_once_with('1', '1234567890')

    @patch('builtins.input', return_value='1234567890')
    def test_return_book(self, mock_input):
        """
        Test returning a book to the library system.

        This test verifies that a book can be returned correctly by calling the checkout manager's return_book method.
        """
        self.library_system.return_book()
        self.checkout_manager.return_book.assert_called_once_with('1234567890')

    @patch('builtins.input', side_effect=['1', '1234567890'])
    def test_search_book(self, mock_input):
        """
        Test searching for a book in the library system.

        This test verifies that a book can be found correctly by calling the book manager's get_book_by_isbn method.
        """
        mock_book = MagicMock()
        mock_book.__str__.return_value = "Test Book"
        self.book_manager.get_book_by_isbn.return_value = mock_book
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library_system.search_book()
            self.assertIn("Test Book", fake_out.getvalue())

    @patch('builtins.input', side_effect=['1', '1'])
    def test_search_user(self, mock_input):
        """
        Test searching for a user in the library system.

        This test verifies that a user can be found correctly by calling the user manager's get_user_by_id method.
        """
        mock_user = MagicMock()
        mock_user.__str__.return_value = "Test User"
        self.user_manager.get_user_by_id.return_value = mock_user
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library_system.search_user()
            self.assertIn("Test User", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()
