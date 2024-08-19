from aifc import Error
import unittest
from unittest.mock import patch, Mock
from src.database_handler import DatabaseHandler

class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.db_handler = DatabaseHandler("localhost", "user", "password", "test_db")

    @patch('src.database_handler.mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        connection = self.db_handler.connect()
        self.assertIsNotNone(connection)

    @patch('src.database_handler.mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        mock_connect.side_effect = Error("Connection failed")
        connection = self.db_handler.connect()
        self.assertIsNone(connection)

    def test_create_table_success(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        result = self.db_handler.create_table(mock_connection)
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()

    def test_create_table_failure(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Error("Table creation failed")
        
        result = self.db_handler.create_table(mock_connection)
        self.assertFalse(result)

    def test_insert_data_success(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        data = {
            "employees": [
                {
                    "empNo": "1", "givenName": "John", "surname": "Doe",
                    "preferredName": "Johnny", "initial": "J", "positionName": "Developer",
                    "positionNameFr": "Développeur", "photoRevision": 1,
                    "active": True, "email": "john@example.com"
                }
            ]
        }
        
        result = self.db_handler.insert_data(mock_connection, data)
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_connection.commit.assert_called_once()

    def test_insert_data_failure(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Error("Insert failed")
        
        data = {"employees": [{"empNo": "1", "givenName": "John"}]}
        
        result = self.db_handler.insert_data(mock_connection, data)
        self.assertFalse(result)
        mock_connection.rollback.assert_called_once()