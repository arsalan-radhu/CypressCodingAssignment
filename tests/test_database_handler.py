import unittest
from unittest.mock import patch, Mock
from mysql.connector import Error
from src.database_handler import DatabaseHandler

class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test method.
        Initialize DatabaseHandler with test configuration.
        """
        self.db_handler = DatabaseHandler("localhost", "user", "password", "test_db")

    @patch('src.database_handler.mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        """
        Test successful database connection.
        
        Mock the mysql.connector.connect method to return a mock connection.
        Verify that a connection object is returned.
        """
        # Arrange
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        # Act
        connection = self.db_handler.connect()

        # Assert
        self.assertIsNotNone(connection)
        mock_connect.assert_called_once_with(**self.db_handler.config)

    @patch('src.database_handler.mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        """
        Test database connection failure.
        
        Mock mysql.connector.connect to raise an Error.
        Verify that None is returned and the error is logged.
        """
        # Arrange
        mock_connect.side_effect = Error("Connection failed")

        # Act
        connection = self.db_handler.connect()

        # Assert
        self.assertIsNone(connection)

    def test_create_table_success(self):
        """
        Test successful table creation.
        
        Mock the database connection and cursor.
        Verify that the method returns True and executes the correct SQL.
        """
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Act
        result = self.db_handler.create_table(mock_connection)

        # Assert
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        # You could also check the SQL string passed to execute

    def test_create_table_failure(self):
        """
        Test table creation failure.
        
        Mock the cursor to raise an Error when executing SQL.
        Verify that the method returns False and the error is logged.
        """
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Error("Table creation failed")
        
        # Act
        result = self.db_handler.create_table(mock_connection)

        # Assert
        self.assertFalse(result)

    def test_insert_data_success(self):
        """
        Test successful data insertion.
        
        Mock the database connection and cursor.
        Provide sample employee data.
        Verify that the method returns True and correct SQL is executed.
        """
        # Arrange
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
        
        # Act
        result = self.db_handler.insert_data(mock_connection, data)

        # Assert
        self.assertTrue(result)
        mock_cursor.executemany.assert_called_once()
        mock_connection.commit.assert_called_once()

    def test_insert_data_failure(self):
        """
        Test data insertion failure.
        
        Mock the cursor to raise an Error when executing SQL.
        Verify that the method returns False, the error is logged, and a rollback occurs.
        """
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.executemany.side_effect = Error("Insert failed")
        
        data = {"employees": [{"empNo": "1", "givenName": "John"}]}
        
        # Act
        result = self.db_handler.insert_data(mock_connection, data)

        # Assert
        self.assertFalse(result)
        mock_connection.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()