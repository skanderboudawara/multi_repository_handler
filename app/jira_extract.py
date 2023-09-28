import csv
import json
import os
import re
import shutil

import requests
from app.logger import logger
from app.utils import (
    copy_modules,
    create_env_file,
    remove_file_batch,
    return_env_tokens,
    show_alert,
    update_env_file,
)

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
print(script_path)


def get_jira_csv():
    create_env_file()
    update_env_file()
    username, requests_ca_bundle, api_token, jira_query, jira_url = return_env_tokens()
    os.environ["REQUESTS_CA_BUNDLE"] = requests_ca_bundle

    # Define the API URL without extra slashes
    api_url = f"{jira_url}rest/api/2/search"

    # Set up HTTP Basic Authentication
    auth = (username, api_token)

    # Define JQL query parameters
    params = {
        "jql": jira_query,
        "maxResults": -1,  # Adjust as needed
        "fields": (
            "key,status,issuetype,summary,customfield_10104,"
            "assignee,customfield_10106"
        ),  # Replace XXXXX with the Story Point field ID
    }

    # Make the Jira API request
    response = requests.get(api_url, auth=auth, params=params)

    if response.status_code == 200:
        data = response.json()["issues"]

        jira_folder = os.path.join(script_path, "jira")
        # Specify the CSV file name
        csv_file = os.path.join(jira_folder, "jira_export.csv")

        if os.path.exists(csv_file):
            # If it exists, open it in write mode to empty it
            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                file.truncate(0)  # Empty the file
        # Write the data to a CSV file
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            csv_writer = csv.writer(file)

            # Write header row
            csv_writer.writerow(
                [
                    "Key",
                    "Status",
                    "Issue Type",
                    "Summary",
                    "Sprint",
                    "Assignee",
                    "Story Point",
                ]
            )

            # Write issue data
            for issue in data:
                key = issue["key"]
                status = issue["fields"]["status"]["name"]
                issue_type = issue["fields"]["issuetype"]["name"]
                summary = issue["fields"]["summary"]

                # Sprint may not always be available, handle it accordingly
                sprint = issue["fields"]["customfield_10104"]
                # Extract the 'name' attribute using regular expression
                if sprint:
                    name_pattern = r"name=([^,]+)"
                    if name_match := re.search(name_pattern, sprint[0]):
                        sprint = name_match[1]
                else:
                    sprint = ""

                # Assignee may not always be available, handle it accordingly
                if "fields" in issue and "assignee" in issue["fields"]:
                    if (
                        issue["fields"]["assignee"] is not None
                        and "displayName" in issue["fields"]["assignee"]
                    ):
                        assignee = issue["fields"]["assignee"]["displayName"]
                    else:
                        assignee = ""
                else:
                    assignee = ""

                # Replace 'customfield_XXXXX' with the actual Story Point field ID
                # You can find the field ID in Jira's advanced settings
                story_point = issue["fields"]["customfield_10106"]

                csv_writer.writerow(
                    [key, status, issue_type, summary, sprint, assignee, story_point]
                )
        show_alert("Jira Data Imported")
        logger(f"Data exported to {csv_file}")
        return csv_file
    else:
        logger(f"Error {response.status_code}: {response.text}")


# Function to search for and extract patterns in a Python file
def extract_patterns(file_path, pattern_set):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        matches = re.findall(r"D2J08EProject-\d{4}", content)
        pattern_set.update(matches)


# Function to recursively search for .py files and extract patterns
def search_and_extract_patterns(root_folder):
    pattern_set = set()

    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(foldername, filename)
                extract_patterns(file_path, pattern_set)

    new_pattern_set = set()
    for pattern in pattern_set:
        if match := re.match(r"D2J08EProject-(\d{4})", pattern):
            new_pattern = f"D2J08EProject-{int(match[1])}"
            new_pattern_set.add(new_pattern)

    return new_pattern_set


# Define a function to extract digits after "eProject Sprint"
def extract_digits(text):
    if isinstance(text, str):
        if match := re.search(r"eProject Sprint (\d+)", text):
            return match[1]
    return ""


def perform_jira_extract():
    all_repositories = None
    try:
        with open(os.path.join(script_path, "app/repos.json"), "r") as json_file:
            all_repositories = json.load(json_file)
    except FileNotFoundError:
        logger("No repos.json file found, creating a new one", "warn")
    all_repositories = list(all_repositories.keys())
    logger("init .env file")
    create_env_file()
    logger("Copying modules ...")
    copy_modules(
        os.path.join(script_path, "remote_repositories"),
        all_repositories,
        os.path.join(script_path, "local_modules"),
    )

    logger("Removing pipeline.py ...")
    remove_file_batch(os.path.join(script_path, "local_modules"), "pipeline.py")

    logger("Removing setup.py ...")
    remove_file_batch(os.path.join(script_path, "local_modules"), "setup.py")

    # Create a docs folder in the current directory
    jira_folder = os.path.join(script_path, "jira")

    try:
        # Remove the folder if it exists
        shutil.rmtree(jira_folder)
        logger(f"Folder '{jira_folder}' removed successfully.")
    except FileNotFoundError:
        logger(f"Folder '{jira_folder}' not found.", "warn")
    except Exception as e:
        logger(f"An error occurred: {str(e)}", "critical")

    os.mkdir(os.path.join(script_path, "jira"))
    get_jira_csv()
