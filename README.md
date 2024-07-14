# Library Management System

This project implements a command-line Library Management System in Python. It manages books, users, and checkouts through an interactive interface.

## Features

- **Book Management**: Add, update, delete, list, and search books by title, author, or ISBN.
- **User Management**: Add, update, delete, list, and search users by name or ID.
- **Checkout System**: Check out and return books, with automatic availability tracking.
- **Data Persistence**: Flexible storage system supporting both file-based (JSON) and in-memory storage.
- **Error Handling**: Comprehensive input validation and error management.
- **Colorful Interface**: User-friendly CLI with color-coded outputs for better readability.



## Project Structure
```
├── library
│   ├── book.py
│   ├── checkout.py
│   ├── storage.py
│   ├── user.py
│   └── __init__.py
├── tests
│   ├── test_book_manager.py
│   ├── test_checkout_manager.py
│   ├── test_library_system.py
│   ├── test_user_manager.py
│   └── __init__.py
├── config.py
├── main.py
└── run_tests.py
```


## Getting Started

To get a local copy of this project and install dependencies:

```bash
git clone https://github.com/saifltr/Library-Management-System.git
```
```bash
cd Library-Management-System
```

Install the dependencies

```bash
pip install -r requirements.txt
```

# Usage
Run the main script to start the Library Management System:

``` bash
python main.py
```

Main Features
- **Manage Books:** Add, update, delete, list, search, checkout, and return books.
- **Manage Users:** Add, update, delete, list, and search users.

# Testing
Unit tests are provided in the tests directory using pytest. To run tests and generate coverage reports:

To run the entire test suites:
```bash
python run_tests.py
```

To run the tests using pytest:
```bash
pytest
```

To get the coverage report of tests:
```bash
coverage run -m pytest
```

```bash
coverage report
```

For detailed HTML Report
```bash
coverage html
```

# Design Principles
- **Object-Oriented Design:** Utilizes classes and inheritance for clear structure and code reuse.
- **Separation of Concerns:** Distinct modules for different functionalities (books, users, checkouts).
- **SOLID Principles:** Adheres to Single Responsibility, Open-Closed, and other SOLID principles.
- **DRY (Don't Repeat Yourself):** Minimizes code duplication through well-structured classes and methods.


