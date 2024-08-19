import csv
from typing import Dict
import logging

def save_to_csv(data: Dict, filename: str = "employees.csv") -> bool:
    """
    Save the given employee data to a CSV file.

    This function takes a dictionary of employee data and writes it to a CSV file.
    It handles file creation, writing headers, and row data.

    Args:
        data (Dict): A dictionary containing an 'employees' key with a list of employee records.
        filename (str, optional): The name of the CSV file to create. Defaults to "employees.csv".

    Returns:
        bool: True if the data was successfully saved, False otherwise.

    Raises:
        IOError: If there's an issue writing to the file.
    """
    # Check if the data is valid and contains employee records
    if not data or "employees" not in data or not data["employees"]:
        logging.warning("No data to save to CSV")
        return False

    try:
        with open(filename, 'w', newline='') as csvfile:
            # Assume all employees have the same structure; use keys from the first employee as fieldnames
            fieldnames = data["employees"][0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header row
            writer.writeheader()
            
            # Write all employee records
            writer.writerows(data["employees"])
        
        logging.info(f"Data successfully saved to {filename}")
        return True
    except IOError as e:
        # Log any file I/O errors
        logging.error(f"Error saving to CSV: {e}")
        return False