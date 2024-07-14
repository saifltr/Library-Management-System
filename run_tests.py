import unittest

# This script is used to run all the unit tests in the project automatically

# Create a TestLoader object
# TestLoader is responsible for loading tests according to various criteria
test_loader = unittest.TestLoader()

# Discover all tests in the 'tests' directory
# This method walks through all files in the specified directory (and subdirectories)
# and loads any tests it finds (files that match the pattern test*.py)
test_suite = test_loader.discover('tests')

# Create a TextTestRunner object
# This runner will execute the tests and output the results to the console
runner = unittest.TextTestRunner()

# Run the discovered tests
# This will execute all the tests found in the 'tests' directory
# and print the results (passes, failures, errors) to the console
runner.run(test_suite)

