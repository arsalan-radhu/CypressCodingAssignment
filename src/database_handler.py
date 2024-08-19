import mysql.connector
from mysql.connector import Error
from typing import Dict, Optional
import logging

class DatabaseHandler:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    def connect(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        Establish a connection to the database.
        
        Returns:
            Optional[mysql.connector.MySQLConnection]: A database connection object if successful, None otherwise.
        """
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            return None

    def create_table(self, connection: mysql.connector.MySQLConnection) -> bool:
        """
        Create the AVANTI_EMPLOYEES table if it doesn't exist.
        
        Args:
            connection (mysql.connector.MySQLConnection): An active database connection.
        
        Returns:
            bool: True if the table was created successfully or already exists, False otherwise.
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

    def insert_data(self, connection: mysql.connector.MySQLConnection, data: Dict) -> bool:
        """
        Insert or update employee data in the AVANTI_EMPLOYEES table.
        
        Args:
            connection (mysql.connector.MySQLConnection): An active database connection.
            data (Dict): The data to insert, expected to have an 'employees' key.
        
        Returns:
            bool: True if the data was inserted successfully, False otherwise.
        """
        insert_query = """
        INSERT INTO AVANTI_EMPLOYEES 
        (empNo, givenName, surname, preferredName, initial, positionName, positionNameFr, photoRevision, active, email) 
        VALUES (%(empNo)s, %(givenName)s, %(surname)s, %(preferredName)s, %(initial)s, %(positionName)s, %(positionNameFr)s, %(photoRevision)s, %(active)s, %(email)s)
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
                cursor.executemany(insert_query, data["employees"])
            connection.commit()
            return True
        except Error as e:
            logging.error(f"Error inserting data: {e}")
            connection.rollback()
            return False