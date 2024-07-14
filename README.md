# Library Management System

This project implements a command-line Library Management System in Python. It manages books, users, and checkouts through an interactive interface.

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
cd Library-Management-System.git
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
- Manage Books: Add, update, delete, list, search, checkout, and return books.
- Manage Users: Add, update, delete, list, and search users.
