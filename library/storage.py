import json
import os

class Storage:
    """
    Handles data storage and retrieval for the library system.

    This class provides methods to save and load data either to/from a file
    or in-memory, depending on the configuration.
    """

    def __init__(self, file_path: str):
        """
        Initialize a Storage instance.

        Args:
            file_path (str): The path to the file where data will be stored.
                             If set to ':memory:', data will be stored in memory.
        """
        self.file_path = file_path
        self.in_memory_data = []

    def save_data(self, data: list):
        """
        Save data either to a file or in memory.

        Args:
            data (list): The data to be saved.
        """
        if self.file_path == ':memory:':
            self.in_memory_data = data
        else:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)

    def load_data(self) -> list:
        """
        Load data either from a file or from memory.

        Returns:
            list: The loaded data.
        """
        if self.file_path == ':memory:':
            return self.in_memory_data
        
        # Check if file exists and is not empty
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return []
        
        with open(self.file_path, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
        return json.loads(content)