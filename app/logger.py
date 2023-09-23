"""
This module contains the logger function.
"""
import datetime
import logging
import os
import sys

# Define the log file name with today's date

# Define the log folder and log file name with today's date
log_folder = "log"
script_path = os.getcwd()
log_folder = os.path.join(script_path, log_folder)
os.makedirs(log_folder, exist_ok=True)
log_file_name = os.path.join(log_folder, f"{datetime.date.today()}_log.txt")
# log_file_name = f"{datetime.date.today()}_log.txt"

# Configure the logging
logging.basicConfig(
    filename=log_file_name,
    level=logging.DEBUG,  # Adjust the log level as needed
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def logger(text, log_type="info"):
    """
    This function logs the text to the log file and prints it to the console.

    :param text: The text to log.

    :param log_type: The type of log. Valid values are "info", "warn", "error", and "critical".

    :return: None
    """
    if log_type not in ["info", "warn", "error", "critical"]:
        raise ValueError("Invalid log type")
    if log_type == "info":
        logging.info(text)
    elif log_type == "warn":
        logging.warning(text)
    elif log_type == "error":
        logging.error(text)
    elif log_type == "critical":
        logging.critical(text)
        sys.exit(1)
    else:
        print("Invalid log type")
    print(text)
