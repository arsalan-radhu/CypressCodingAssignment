import unittest
import os
from src.csv_handler import save_to_csv

class TestCSVHandler(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test method.
        Define a test filename for CSV output.
        """
        self.test_filename = "test_employees.csv"

    def tearDown(self):
        """
        Clean up after each test method.
        Remove the test CSV file if it exists.
        """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_save_to_csv_success(self):
        """
        Test successful CSV file creation with valid data.
        
        Provide sample employee data and verify that:
        1. The function returns True (indicating success)
        2. The CSV file is created
        """
        # Arrange
        data = {
            "employees": [
                {"empNo": "1", "name": "John Doe"},
                {"empNo": "2", "name": "Jane Smith"}
            ]
        }

        # Act
        result = save_to_csv(data, self.test_filename)

        # Assert
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_filename))

    def test_save_to_csv_empty_data(self):
        """
        Test CSV file creation with empty employee data.
        
        Provide an empty employees list and verify that:
        1. The function returns True
        2. An empty CSV file (with headers) is created
        """
        # Arrange
        data = {"employees": []}

        # Act
        result = save_to_csv(data, self.test_filename)

        # Assert
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_filename))
        with open(self.test_filename, 'r') as f:
            content = f.read()
            self.assertEqual(content, "\n")  # Only newline (header row)

    def test_save_to_csv_no_employees_key(self):
        """
        Test handling of invalid data structure (missing 'employees' key).
        
        Provide data without 'employees' key and verify that:
        1. The function returns False
        2. No CSV file is created
        """
        # Arrange
        data = {"other_data": []}

        # Act
        result = save_to_csv(data, self.test_filename)

        # Assert
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.test_filename))

    def test_save_to_csv_file_permission_error(self):
        """
        Test handling of file permission errors.
        
        Attempt to save to a protected location and verify that:
        1. The function returns False
        2. The error is logged (would require checking logs)
        """
        # Arrange
        data = {
            "employees": [
                {"empNo": "1", "name": "John Doe"}
            ]
        }

        # Act
        result = save_to_csv(data, "/root/test.csv")

        # Assert
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()