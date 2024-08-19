import csv
from typing import Dict
import logging

def save_to_csv(data: Dict, filename: str = "employees.csv") -> bool:
    """
    Save the given data to a CSV file.
    
    Args:
        data (Dict): The data to save, expected to have an 'employees' key.
        filename (str): The name of the file to save the data to.
    
    Returns:
        bool: True if the data was successfully saved, False otherwise.
    """
    if not data or "employees" not in data or not data["employees"]:
        logging.warning("No data to save to CSV")
        return False

    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = data["employees"][0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(data["employees"])
        
        logging.info(f"Data saved to {filename}")
        return True
    except IOError as e:
        logging.error(f"Error saving to CSV: {e}")
        return False