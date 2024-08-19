import os
import logging
from typing import Dict
from dotenv import load_dotenv
from src.api_client import APIClient
from src.csv_handler import save_to_csv
from src.database_handler import DatabaseHandler

# Load environment variables
load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "https://myavanti.ca/avtesting-api/v1/Employees")
HEADERS = {
    "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
    "Content-Type": "application/json"
}
CSV_FILENAME = os.getenv("CSV_FILENAME", "employees.csv")
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Request payload
PAYLOAD: Dict = {
    "skip": 0,
    "take": 100,
    "empNoReference": "",
    "search": "",
    "total": True,
    "active": 1,
    "sortOrder": 0,
    "sortDirection": 0,
    "takeOption": 0,
    "locations": [],
    "employmentStatus": [],
    "positions": [],
    "sortDefinitions": []
}

def main() -> None:
    """
    Main function to orchestrate the data retrieval, CSV writing, and database insertion process.
    """
    logging.basicConfig(level=logging.INFO)

    # Initialize API client
    api_client = APIClient(API_URL, HEADERS)

    # Query API
    logging.info("Querying API...")
    data = api_client.query_api(PAYLOAD)

    if not data:
        logging.error("Failed to retrieve data from API. Exiting.")
        return

    # Save to CSV
    logging.info("Saving data to CSV...")
    csv_success = save_to_csv(data, CSV_FILENAME)
    if csv_success:
        logging.info(f"Data saved to {CSV_FILENAME}")
    else:
        logging.error("Failed to save data to CSV")

    # Initialize database handler
    db_handler = DatabaseHandler(**DB_CONFIG)

    # Connect to database
    logging.info("Connecting to database...")
    with db_handler.connect() as connection:
        if not connection:
            logging.error("Failed to connect to database. Exiting.")
            return

        # Create table
        logging.info("Creating table if not exists...")
        table_created = db_handler.create_table(connection)
        if not table_created:
            logging.error("Failed to create table. Exiting.")
            return

        # Insert data
        logging.info("Inserting data into database...")
        insert_success = db_handler.insert_data(connection, data)
        if insert_success:
            logging.info("Data successfully inserted into database")
        else:
            logging.error("Failed to insert data into database")

    logging.info("Process completed.")

if __name__ == "__main__":
    main()