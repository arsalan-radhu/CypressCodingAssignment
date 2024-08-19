import unittest
import os
from unittest.mock import patch
from src.csv_handler import save_to_csv

class TestCSVHandler(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_employees.csv"

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_save_to_csv_success(self):
        data = {
            "employees": [
                {"empNo": "1", "name": "John Doe"},
                {"empNo": "2", "name": "Jane Smith"}
            ]
        }
        result = save_to_csv(data, self.test_filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_filename))

    def test_save_to_csv_empty_data(self):
        data = {"employees": []}
        result = save_to_csv(data, self.test_filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_filename))

    def test_save_to_csv_no_employees_key(self):
        data = {"other_data": []}
        result = save_to_csv(data, self.test_filename)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.test_filename))

    def test_save_to_csv_file_permission_error(self):
        data = {
            "employees": [
                {"empNo": "1", "name": "John Doe"}
            ]
        }
        with patch('builtins.open', side_effect=PermissionError):
            result = save_to_csv(data, "/root/test.csv")
            self.assertFalse(result)