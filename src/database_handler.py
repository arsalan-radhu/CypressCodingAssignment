import csv
import mysql.connector
from mysql.connector import Error
from typing import Dict, Optional
import logging

class DatabaseHandler:
    """
    Handles database operations for storing employee data.

    This class manages the connection to a MySQL database and provides methods
    for creating tables and inserting employee data.
    """

    def __init__(self, host: str, user: str, password: str, database: str):
        """
        Initialize the DatabaseHandler with connection parameters.

        Args:
            host (str): The database server host.
            user (str): The database user.
            password (str): The database password.
            database (str): The name of the database to use.
        """
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    def connect(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        Establish a connection to the MySQL database.

        Returns:
            Optional[mysql.connector.MySQLConnection]: A database connection object if successful, None otherwise.

        Raises:
            mysql.connector.Error: If connection fails.
        """
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            return None

    def create_table(self, connection: mysql.connector.MySQLConnection) -> bool:
        """
        Create the AVANTI_EMPLOYEES table if it doesn't exist.

        This method defines the schema for the employee table and executes the CREATE TABLE query.

        Args:
            connection (mysql.connector.MySQLConnection): An active database connection.

        Returns:
            bool: True if the table was created successfully or already exists, False otherwise.

        Raises:
            mysql.connector.Error: If there's an error executing the SQL query.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS AVANTI_EMPLOYEES (
            empNo VARCHAR(255) PRIMARY KEY,
            givenName VARCHAR(255),
            surname VARCHAR(255),
            preferredName VARCHAR(255),
            initial VARCHAR(10),
            positionName VARCHAR(255),
            positionNameFr VARCHAR(255),
            photoRevision INT,
            active BOOLEAN,
            email VARCHAR(255)
        )
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(create_table_query)
            return True
        except Error as e:
            logging.error(f"Error creating table: {e}")
            return False


    # def insert_data(self, connection: mysql.connector.MySQLConnection, data: Dict) -> bool:
    #     """
    #     Insert or update employee data in the AVANTI_EMPLOYEES table.

    #     This method uses an INSERT ... ON DUPLICATE KEY UPDATE query to handle both
    #     new insertions and updates to existing records.

    #     Args:
    #         connection (mysql.connector.MySQLConnection): An active database connection.
    #         data (Dict): The data to insert, expected to have an 'employees' key with a list of employee records.

    #     Returns:
    #         bool: True if the data was inserted successfully, False otherwise.

    #     Raises:
    #         mysql.connector.Error: If there's an error executing the SQL query.
    #     """
    #     insert_query = """
    #     INSERT INTO AVANTI_EMPLOYEES 
    #     (empNo, givenName, surname, preferredName, initial, positionName, positionNameFr, photoRevision, active, email) 
    #     VALUES (%(empNo)s, %(givenName)s, %(surname)s, %(preferredName)s, %(initial)s, %(positionName)s, %(positionNameFr)s, %(photoRevision)s, %(active)s, %(email)s)
    #     ON DUPLICATE KEY UPDATE
    #     givenName = VALUES(givenName),
    #     surname = VALUES(surname),
    #     preferredName = VALUES(preferredName),
    #     initial = VALUES(initial),
    #     positionName = VALUES(positionName),
    #     positionNameFr = VALUES(positionNameFr),
    #     photoRevision = VALUES(photoRevision),
    #     active = VALUES(active),
    #     email = VALUES(email)
    #     """
    #     try:
    #         with connection.cursor() as cursor:
    #             # Execute the query for each employee record
    #             cursor.executemany(insert_query, data["employees"])
    #         connection.commit()
    #         return True
    #     except Error as e:
    #         logging.error(f"Error inserting data: {e}")
    #         connection.rollback()
    #         return False
        
    def insert_data_from_csv(self, connection: mysql.connector.MySQLConnection, csv_filename: str) -> bool:
        insert_query = """
        INSERT INTO AVANTI_EMPLOYEES 
        (empNo, givenName, surname, preferredName, initial, positionName, positionNameFr, photoRevision, active, email) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        givenName = VALUES(givenName),
        surname = VALUES(surname),
        preferredName = VALUES(preferredName),
        initial = VALUES(initial),
        positionName = VALUES(positionName),
        positionNameFr = VALUES(positionNameFr),
        photoRevision = VALUES(photoRevision),
        active = VALUES(active),
        email = VALUES(email)
        """
        try:
            with connection.cursor() as cursor:
                with open(csv_filename, 'r') as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    for row in csv_reader:
                        # Convert 'active' to boolean and 'photoRevision' to int
                        row['active'] = row['active'].lower() == 'true'
                        row['photoRevision'] = int(row['photoRevision'])
                        cursor.execute(insert_query, (
                            row['empNo'], row['givenName'], row['surname'], row['preferredName'],
                            row['initial'], row['positionName'], row['positionNameFr'],
                            row['photoRevision'], row['active'], row['email']
                        ))
            connection.commit()
            return True
        except Error as e:
            logging.error(f"Error inserting data: {e}")
            connection.rollback()
            return False
        except IOError as e:
            logging.error(f"Error reading CSV file: {e}")
            return False   