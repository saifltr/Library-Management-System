import unittest
from unittest.mock import patch, MagicMock
from library.managers.user_manager import UserManager
from library.user import User

class TestUserManager(unittest.TestCase):
    """
    Unit test case for the UserManager class.

    This test case verifies the functionality of the UserManager class,
    ensuring that user management operations are handled correctly.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes a mock storage object and creates an instance of UserManager
        with this mock storage. It also resets the user list and the next user ID for each test.
        """
        self.mock_storage = MagicMock()
        self.user_manager = UserManager()
        self.user_manager.storage = self.mock_storage
        self.user_manager.users = []
        self.user_manager.next_id = 1  # Reset next_id for each test

    def test_add_user(self):
        """
        Test adding a user to the user manager.

        This test verifies that a user can be added correctly, checking the user list size,
        the user's name, and the assigned user ID.
        """
        user = self.user_manager.add_user("Test User")
        self.assertEqual(len(self.user_manager.users), 1)
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.user_id, "1")

    def test_add_user_no_name(self):
        """
        Test adding a user without a name.

        This test verifies that adding a user with an empty name raises a ValueError.
        """
        with self.assertRaises(ValueError):
            self.user_manager.add_user("")

    def test_get_user_by_id(self):
        """
        Test retrieving a user by their ID.

        This test verifies that a user can be retrieved correctly by their ID.
        """
        self.user_manager.add_user("Test User")
        user = self.user_manager.get_user_by_id("1")
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Test User")

    def test_get_user_by_id_not_found(self):
        """
        Test retrieving a user by an invalid ID.

        This test verifies that attempting to retrieve a user with a non-existent ID returns None.
        """
        user = self.user_manager.get_user_by_id("999")
        self.assertIsNone(user)

    def test_list_users(self):
        """
        Test listing all users.

        This test verifies that the list of users is correctly retrieved and contains the expected users.
        """
        self.user_manager.add_user("User 1")
        self.user_manager.add_user("User 2")
        users = self.user_manager.list_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].name, "User 1")
        self.assertEqual(users[1].name, "User 2")

    def test_update_user(self):
        """
        Test updating a user's name.

        This test verifies that a user's name can be updated correctly by their ID.
        """
        self.user_manager.add_user("Old Name")
        updated_user = self.user_manager.update_user("1", "New Name")
        self.assertEqual(updated_user.name, "New Name")

    def test_update_user_not_found(self):
        """
        Test updating a user with an invalid ID.

        This test verifies that attempting to update a user with a non-existent ID raises a ValueError.
        """
        with self.assertRaises(ValueError):
            self.user_manager.update_user("999", "New Name")

    def test_delete_user(self):
        """
        Test deleting a user by their ID.

        This test verifies that a user can be deleted correctly by their ID.
        """
        self.user_manager.add_user("Test User")
        self.user_manager.delete_user("1")
        self.assertEqual(len(self.user_manager.users), 0)

    def test_delete_user_not_found(self):
        """
        Test deleting a user with an invalid ID.

        This test verifies that attempting to delete a user with a non-existent ID raises a ValueError.
        """
        with self.assertRaises(ValueError):
            self.user_manager.delete_user("999")

    def test_search_users(self):
        """
        Test searching for users by a name substring.

        This test verifies that users can be searched correctly by a substring of their name.
        """
        self.user_manager.add_user("John Doe")
        self.user_manager.add_user("Jane Smith")
        results = self.user_manager.search_users("John")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")

    def test_search_users_case_insensitive(self):
        """
        Test case-insensitive search for users by a name substring.

        This test verifies that users can be searched correctly by a case-insensitive substring of their name.
        """
        self.user_manager.add_user("John Doe")
        results = self.user_manager.search_users("john")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")

    def test_save_users(self):
        """
        Test saving users to storage.

        This test verifies that users can be saved correctly to the storage, checking the data format.
        """
        self.user_manager.add_user("Test User")
        self.mock_storage.save_data.reset_mock()  # Reset the mock after add_user
        self.user_manager.save_users()
        self.mock_storage.save_data.assert_called_once()
        saved_data = self.mock_storage.save_data.call_args[0][0]
        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data[0]['name'], "Test User")

    @patch('library.user.User.from_dict')
    def test_load_users(self, mock_from_dict):
        """
        Test loading users from storage.

        This test verifies that users can be loaded correctly from the storage, checking the data format.
        """
        mock_user = MagicMock(spec=User)
        mock_from_dict.return_value = mock_user
        self.mock_storage.load_data.return_value = [{'name': 'Test User', 'user_id': '1'}]
        
        users = self.user_manager._load_users()
        
        self.assertEqual(len(users), 1)
        self.assertIs(users[0], mock_user)
        mock_from_dict.assert_called_once_with({'name': 'Test User', 'user_id': '1'})

    def test_get_next_id(self):
        """
        Test generating the next user ID.

        This test verifies that the next user ID is generated correctly, considering existing users.
        """
        self.user_manager.users = [
            User("User 1", "1"),
            User("User 2", "2"),
            User("User 3", "3")
        ]
        next_id = self.user_manager._get_next_id()
        self.assertEqual(next_id, 4)

    def test_get_next_id_empty_users(self):
        """
        Test generating the next user ID when there are no users.

        This test verifies that the next user ID is correctly set to 1 when there are no existing users.
        """
        next_id = self.user_manager._get_next_id()
        self.assertEqual(next_id, 1)

if __name__ == '__main__':
    unittest.main()
