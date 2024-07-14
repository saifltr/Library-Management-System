import os

# Determine if the application is running in testing mode
# This is set by checking the 'TESTING' environment variable
# If 'TESTING' is not set or is set to 'False', TESTING will be False
# If 'TESTING' is set to 'True', TESTING will be True
TESTING = os.environ.get('TESTING', 'False') == 'True'

# Get the absolute path of the directory containing this file
# This ensures that file paths are correct regardless of where the script is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure storage locations based on whether we're in testing mode or not
if TESTING:
    # In testing mode, use in-memory storage
    # This is faster for tests and doesn't affect the actual data files
    BOOKS_STORAGE_FILE = ':memory:'
    USERS_STORAGE_FILE = ':memory:'
    CHECKOUTS_STORAGE_FILE = ':memory:'
else:
    # In production mode, use JSON files for persistent storage
    # os.path.join is used to create cross-platform compatible file paths
    BOOKS_STORAGE_FILE = os.path.join(BASE_DIR, 'books_data.json')
    USERS_STORAGE_FILE = os.path.join(BASE_DIR, 'users_data.json')
    CHECKOUTS_STORAGE_FILE = os.path.join(BASE_DIR, 'checkouts_data.json')

