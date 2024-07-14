class User:
    """
    Represents a user in the library system.

    This class manages user information, including name and user ID.
    """

    def __init__(self, name: str, user_id: str):
        """
        Initialize a User.

        Args:
            name (str): The name of the user.
            user_id (str): The unique identifier for the user.
        """
        self.name = name
        self.user_id = user_id

    def __str__(self) -> str:
        """
        Return a string representation of the user.

        Returns:
            str: A string containing the user's name and ID.
        """
        return f"{self.name} (ID: {self.user_id})"

    def to_dict(self) -> dict:
        """
        Convert the user to a dictionary.

        Returns:
            dict: A dictionary containing the user's data.
        """
        return {
            "name": self.name,
            "user_id": self.user_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a User instance from a dictionary.

        Args:
            data (dict): A dictionary containing the user's data.

        Returns:
            User: A new User instance created from the provided data.
        """
        return cls(data["name"], data["user_id"])