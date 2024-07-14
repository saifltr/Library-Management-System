from library.user import User
from library.storage import Storage
import config

class UserManager:
    """
    Manages the users in the library system.

    This class handles operations such as adding, updating, deleting,
    and searching for users, as well as persisting user data.
    """

    def __init__(self):
        """Initialize the UserManager."""
        self.storage = Storage(config.USERS_STORAGE_FILE)
        self.users = self._load_users()
        self.next_id = self._get_next_id()

    def _load_users(self) -> list:
        """
        Load users from storage.

        Returns:
            list: A list of User objects.
        """
        data = self.storage.load_data()
        return [User.from_dict(user_data) for user_data in data]

    def _get_next_id(self) -> int:
        """
        Determine the next available user ID.

        Returns:
            int: The next available user ID.
        """
        if not self.users:
            return 1
        return max(int(user.user_id) for user in self.users) + 1

    def save_users(self):
        """Save the current list of users to storage."""
        self.storage.save_data([user.to_dict() for user in self.users])

    def add_user(self, name: str) -> User:
        """
        Add a new user to the library system.

        Args:
            name (str): The name of the new user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If the name is empty.
        """
        if not name:
            raise ValueError("User name is required.")
        user_id = str(self.next_id)
        user = User(name, user_id)
        self.users.append(user)
        self.next_id += 1
        self.save_users()
        return user

    def get_user_by_id(self, user_id: str) -> User:
        """
        Retrieve a user by their ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            User: The User object with the given ID, or None if not found.
        """
        return next((user for user in self.users if user.user_id == user_id), None)

    def list_users(self) -> list:
        """
        Get a list of all users in the library system.

        Returns:
            list: A list of all User objects.
        """
        return self.users

    def update_user(self, user_id: str, name: str) -> User:
        """
        Update a user's information.

        Args:
            user_id (str): The ID of the user to update.
            name (str): The new name for the user.

        Returns:
            User: The updated User object.

        Raises:
            ValueError: If the user with the given ID is not found.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        user.name = name
        self.save_users()
        return user

    def delete_user(self, user_id: str):
        """
        Delete a user from the library system.

        Args:
            user_id (str): The ID of the user to delete.

        Raises:
            ValueError: If the user with the given ID is not found.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        self.users.remove(user)
        self.save_users()

    def search_users(self, name: str) -> list:
        """
        Search for users by name.

        Args:
            name (str): The name (or part of the name) to search for.

        Returns:
            list: A list of User objects that match the search criteria.
        """
        name = name.lower()
        return [user for user in self.users if name in user.name.lower()]