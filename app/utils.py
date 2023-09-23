"""
This module contains utility functions used by the main script.
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import zipfile

from app.logger import logger

script_path = os.getcwd()
print(script_path)


def print_centered_text(text):
    """
    This function prints the text centered in a box of '#' characters.

    :param text: The text to be printed

    :return: None
    """
    if not isinstance(text, str):
        raise TypeError("Invalid text type")
    # Calculate the width of the box
    box_width = len(text) + 8  # You can adjust this to fit your text

    # Calculate the number of spaces needed to center the text
    spaces = (box_width - len(text) - 2) // 2

    # Create the left and right padding strings
    left_padding = " " * spaces
    right_padding = " " * (box_width - len(text) - len(left_padding) - 2)

    # Build the final string and print it
    centered_text = (
        f"{'#' * box_width}\n#{left_padding}{text}{right_padding}#\n{'#' * box_width}"
    )
    print(centered_text)


def log_and_process(to_be_processed, log_type="info"):
    """
    This function logs the command to be executed and then executes it.

    :param to_be_processed: The command to be executed

    :param log_type: The type of log to be used. Default is 'info'

    :return: None
    """
    if not isinstance(to_be_processed, list):
        raise TypeError("Invalid type for to_be_processed")
    if not isinstance(log_type, str):
        raise TypeError("Invalid type for log_type")
    logger(" ".join(to_be_processed), log_type)
    subprocess.run(to_be_processed)


def git_checkout_pull(directory, checkout_branch):
    """
    This function performs a git checkout master and git pull in the specified directory.

    :param directory: The directory where the git checkout master and git pull should be performed

    :param checkout_branch: The branch to checkout

    :return: None
    """
    if not isinstance(directory, str):
        raise TypeError("Invalid type for directory")
    if not isinstance(checkout_branch, str):
        raise TypeError("Invalid type for checkout_branch")
    # Change the working directory to the directory we want to operate on
    os.chdir(directory)

    # Run git checkout master
    log_and_process(["git", "checkout", checkout_branch])

    # Run git pull
    log_and_process(["git", "pull"])


def clone_repository_git(repo_url, clone_folder):
    """
    This function clones a repository using git.

    :param repo_url: The URL of the repository to clone

    :param clone_folder: The folder where the repository should be cloned

    :return: None
    """
    if not isinstance(repo_url, str):
        raise TypeError("Invalid type for repo_url")
    if not isinstance(clone_folder, str):
        raise TypeError("Invalid type for clone_folder")
    log_and_process(["git", "clone", repo_url])


def git_create_branch_if_not_exist(directory, new_branch, base_branch):
    """
    This function performs a git checkout -b to create a new branch if it doesn't already exist.

    :param directory: The directory where the git checkout -b should be performed

    :param new_branch: The name of the new branch

    :param base_branch: The name of the base branch

    :return: None
    """
    if not isinstance(directory, str):
        raise TypeError("Invalid type for directory")
    if not isinstance(new_branch, str):
        raise TypeError("Invalid type for new_branch")
    if not isinstance(base_branch, str):
        raise TypeError("Invalid type for base_branch")
    # Change the working directory to the directory we want to operate on
    os.chdir(directory)

    # Check if the branch already exists
    branch_exists = (
        subprocess.run(["git", "show-ref", "--quiet", "--heads", new_branch]).returncode
        == 0
    )

    if not branch_exists:
        log_and_process(["git", "checkout", base_branch])
        log_and_process(["git", "pull"])

        # Run git checkout -b to create the branch
        log_and_process(["git", "checkout", "-b", new_branch, base_branch])

        log_and_process(["git", "push", "-u", "origin", new_branch])

        log_and_process(["git", "pull"])
    else:
        log_and_process(["git", "checkout", new_branch])
        log_and_process(["git", "pull"])

        logger(f"Branch '{new_branch}' already exists.")


def create_branch_if_not_exist(
    root_directory, all_repositories, new_branch, base_branch
):
    """
    This function creates a new branch in all repositories if it doesn't already exist.

    :param root_directory: The root directory where the repositories are located

    :param all_repositories: The list of all repositories

    :param new_branch: The name of the new branch

    :param base_branch: The name of the base branch

    :return: None
    """
    if not isinstance(root_directory, str):
        raise TypeError("Invalid type for root_directory")
    if not isinstance(all_repositories, list):
        raise TypeError("Invalid type for all_repositories")
    if not isinstance(new_branch, str):
        raise TypeError("Invalid type for new_branch")
    if not isinstance(base_branch, str):
        raise TypeError("Invalid type for base_branch")
    # Walk through all directories in the root_directory
    for repo in all_repositories:
        print_centered_text(repo)
        # Join the root and repo to get the complete repo path
        current_repo = os.path.join(root_directory, repo)

        # Check if the repo contains a .git subrepo (i.e., it's a Git repository)
        if os.path.exists(os.path.join(current_repo, ".git")):
            logger(f"Processing repository in {current_repo}")

            # Perform git checkout master and git pull
            try:
                git_create_branch_if_not_exist(current_repo, new_branch, base_branch)
            except Exception as e:
                logger(f"Failed to process repository in {current_repo}", "error")
                logger(e, "critical")


def update_all_local_repositories(root_directory, all_repositories, checkout_branch):
    """
    This function performs a git checkout and git pull in all repositories.

    :param root_directory: The root directory where the repositories are located

    :param all_repositories: The list of all repositories

    :param checkout_branch: The name of the branch to checkout

    :return: None
    """

    if not isinstance(root_directory, str):
        raise TypeError("Invalid type for root_directory")
    if not isinstance(all_repositories, list):
        raise TypeError("Invalid type for all_repositories")
    if not isinstance(checkout_branch, str):
        raise TypeError("Invalid type for checkout_branch")
    # Walk through all directories in the root_directory
    for repo in all_repositories:
        print_centered_text(repo)
        # Join the root and repo to get the complete repo path
        current_repo = os.path.join(root_directory, repo)

        # Check if the repo contains a .git subrepo (i.e., it's a Git repository)
        if os.path.exists(os.path.join(current_repo, ".git")):
            logger(f"Processing repository in {current_repo}")

            # Perform git checkout master and git pull
            try:
                git_checkout_pull(current_repo, checkout_branch)
            except Exception as e:
                logger(f"Failed to process repository in {current_repo}", "error")
                logger(e, "critical")


def remove_directory_if_exists(directory_path):
    """
    This function removes the specified directory if it exists.

    :param directory_path: The path of the directory to remove

    :return: None
    """
    if not isinstance(directory_path, str):
        raise TypeError("Invalid type for directory_path")
    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
            logger(f"Removed directory: {directory_path}")
        except Exception as e:
            logger(f"Failed to remove directory: {directory_path}", "error")
            logger(e, "critical")
    else:
        logger(f"Directory not found: {directory_path}", "warn")


def copy_modules(root_directory, all_repositories, destination_directory):
    """
    This function copies the folder_package from each repository to the destination directory.

    :param root_directory: The root directory where the repositories are located

    :param all_repositories: The list of all repositories

    :param destination_directory: The destination directory where the folder_package should be copied

    :return: None
    """
    # Destination directory where you want to copy the folder_package

    # Loop through each repository
    for repo_name in all_repositories:
        print_centered_text(repo_name)

        # Construct the source path for the folder_package
        source_directory = os.path.join(root_directory, repo_name)

        print(source_directory)

        # Check if the directory "transforms-python" exists within source_directory
        def exists_and_isdir(source_directory, folder):
            return os.path.exists(
                os.path.join(source_directory, folder)
            ) and os.path.isdir(os.path.join(source_directory, folder))

        # if exists_and_isdir(source_directory, "database"):
        #     source_directory = os.path.join(source_directory, "database")
        #     get_package = [""]

        if exists_and_isdir(source_directory, "transforms-python"):
            source_directory = os.path.join(source_directory, "transforms-python")

        if exists_and_isdir(source_directory, "src"):
            source_directory = os.path.join(source_directory, "src")

            logger(f"Copying folder_package from {source_directory}")
            # print(source_directory)
            get_all_folders = [
                folder
                for folder in os.listdir(source_directory)
                if os.path.isdir(os.path.join(source_directory, folder))
            ]

            get_package = [
                folder
                for folder in get_all_folders
                if folder
                not in ["expectations", "test", ".ruff_cache", "__pycache__", "tests"]
            ]
        source_directory = os.path.join(source_directory, rf"{get_package[0]}")
        logger(f"Copying folder_package from {get_package[0]}")
        logger(source_directory)
        # Check if the source directory exists
        if os.path.exists(source_directory):
            # Construct the destination path

            folder_destination = os.path.join(destination_directory, repo_name)
            logger(folder_destination)

            if os.path.exists(folder_destination):
                shutil.rmtree(folder_destination)
            # Copy the folder_package to the destination directory
            try:
                log_and_process(
                    ["robocopy", source_directory, folder_destination, "/MIR"]
                )
                # shutil.copytree(source_directory, folder_destination, dirs_exist_ok = True)
                logger(
                    f"Successfully copied {repo_name}'s folder_package to {destination_directory}"
                )
            except Exception as e:
                logger(
                    f"Failed to copy {repo_name}'s folder_package to {destination_directory}",
                    "warn",
                )
                logger(e, "critical")

        else:
            logger(
                f"Source directory for {repo_name}'s folder_package not found. Skipping...",
                "warn",
            )

    init_file_path = os.path.join(destination_directory, "__init__.py")

    # Create the __init__.py file
    with open(init_file_path, "w", encoding="utf-8"):
        pass


def change_version(file_conf, new_version):
    """
    This function changes the version in the specified file.

    :param file_conf: The path of the file to update

    :param new_version: The new version to use

    :return: None
    """
    # Read the contents of file1.py
    with open(file_conf, "r") as file:
        file_contents = file.read()

    # Use regex to replace the values
    file_contents = re.sub(
        r'version = "[^"]+"', f'version = "{new_version}"', file_contents
    )
    file_contents = re.sub(
        r'release = "[^"]+"', f'release = "{new_version}"', file_contents
    )

    # Write the updated contents back to file1.py
    with open(file_conf, "w") as file:
        file.write(file_contents)
        logger(f"Updated version to {new_version} in {file_conf}")


# Function to remove the specified file
def remove_file(file_path):
    """
    This function removes the specified file.

    :param file_path: The path of the file to remove

    :return: None
    """
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error removing {file_path}: {e}")


def remove_file_batch(packages_local, file_to_remove):
    """
    This function removes the specified file from the specified directory.

    :param packages_local: The directory where the file should be removed

    :param file_to_remove: The name of the file to remove
    """
    # Traverse directories and subdirectories
    for root, dirs, files in os.walk(packages_local):
        for file in files:
            if file == file_to_remove:
                file_path = os.path.join(root, file)
                remove_file(file_path)
    logger(f"{file_to_remove} is removed!")


def create_zip_file(password):
    """
    This function creates a ZIP file with password protection.

    :param password: The password to use for the ZIP file

    :return: None
    """
    if not isinstance(password, str):
        raise TypeError("Invalid type for password")
    # Directory to be zipped
    logger("Creating Zip File")
    source_directory = os.path.join(script_path, "docs", "build")

    if not os.path.exists(os.path.join(script_path, "builds")):
        os.mkdir(os.path.join(script_path, "builds"))

    formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Name of the output ZIP file
    destination_directory = os.path.join(
        script_path, "builds", f"build_{str(formatted_datetime)}.zip"
    )

    try:
        # Create a ZIP file with password protection
        with zipfile.ZipFile(destination_directory, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add all files and subdirectories in the directory to the ZIP file
            for foldername, subfolders, filenames in os.walk(source_directory):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, source_directory)
                    zipf.write(
                        file_path, arcname=arcname, compress_type=zipfile.ZIP_DEFLATED
                    )

        # Add a password to the ZIP file
        zipf.setpassword(bytes(password, "utf-8"))
        logger(f'ZIP file "{destination_directory}" created with password protection.')
        return destination_directory, os.path.join(script_path, "builds")
    except Exception as e:
        logger(f"An error occurred: {str(e)}", "critical")


def copy_file(source_file, destination_file):
    """
    This function copies the specified file to the specified destination.

    :param source_file: The path of the file to copy

    :param destination_file: The path of the destination

    :return: None
    """
    source_file_path = os.path.join(source_file)
    destination_file_path = os.path.join(destination_file)

    try:
        # Copy the file from source to destination, overwriting if it already exists
        shutil.copy2(source_file_path, destination_file_path)
        logger(f"File '{source_file}' copied and replaced successfully.")
    except FileNotFoundError:
        logger(f"File '{source_file}' not found in the source directory.", "critical")
    except Exception as e:
        logger(f"An error occurred: {str(e)}", "critical")


def commit_push(all_repositories, branch_name, commit_message):
    """
    This function commits and pushes the changes to the remote repository.

    :param repository_path: The path of the repository

    :param branch_name: The name of the branch to commit and push

    :param commit_message: The commit message

    :return: None
    """
    for repo in all_repositories:
        # Join the root and repo to get the complete repo path
        current_repo = os.path.join(script_path, "remote_repositories", repo)

        try:
            # Change to the repository directory
            os.chdir(current_repo)

            # Checkout the branch
            log_and_process(["git", "checkout", branch_name])

            # Stage all modifications
            log_and_process(["git", "add", "."])

            # Commit all modifications
            log_and_process(["git", "commit", "-m", commit_message])

            # Push the branch to the remote repository
            log_and_process(["git", "push", "origin", branch_name])

        except subprocess.CalledProcessError as e:
            logger(f"Error in repository {current_repo}: {e}", "critical")


def scan_all_repositories():
    root_directory = os.path.join(script_path, "remote_repositories")

    # List all entries (both files and directories) in the root directory
    all_entries = os.listdir(root_directory)

    # Filter the list to include only directories
    directories_only = [
        entry
        for entry in all_entries
        if os.path.isdir(os.path.join(root_directory, entry))
    ]

    f_repo_json = os.path.join(script_path, "app/repos.json")

    try:
        with open(f_repo_json, "r") as json_file:
            repos_data = json.load(json_file)
    except FileNotFoundError:
        repos_data = {}
        logger("No repos.json file found, creating a new one", "warn")

    for repo in directories_only:
        if repo not in repos_data.keys():
            repos_data[repo] = "No URL found"
            logger(f"Added {repo} to repos.json")
    with open(f_repo_json, "w") as json_file:
        json.dump(repos_data, json_file, indent=4)
