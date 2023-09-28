import datetime
import os
import shutil
import zipfile

from app.logger import logger
from app.utils import (
    change_version,
    copy_file,
    copy_modules,
    log_and_process,
    remove_file_batch,
)

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
print(script_path)


def remove_docs():
    """
    This function removes the docs folder.

    :param: None

    :return: None
    """
    # Create a docs folder in the current directory
    docs_folder_path = os.path.join(script_path, "docs")

    try:
        # Remove the folder if it exists
        shutil.rmtree(docs_folder_path)
        logger(f"Folder '{docs_folder_path}' removed successfully.")
    except FileNotFoundError:
        logger(f"Folder '{docs_folder_path}' not found.", "warn")
    except Exception as e:
        logger(f"An error occurred: {str(e)}", "critical")
    os.mkdir(docs_folder_path)
    os.mkdir(os.path.join(docs_folder_path, "source"))
    os.mkdir(os.path.join(docs_folder_path, "build"))
    logger(f"Created 'docs' folder in {script_path}")


def preparing_files_and_folders_sphinx(all_repositories, model_progress_bar):
    """
    This function prepares the files and folders for the documentation generation.

    :param all_repositories: The list of all repositories.

    :param model_progress_bar: The progress bar to update.

    :return: The path of the zip file.
    """
    logger("Copying modules ...")
    copy_modules(
        os.path.join(script_path, "remote_repositories"),
        all_repositories,
        os.path.join(script_path, "local_modules"),
        model_progress_bar,
    )

    logger("Removing pipeline.py ...")
    remove_file_batch(os.path.join(script_path, "local_modules"), "pipeline.py")

    logger("Removing setup.py ...")
    remove_file_batch(os.path.join(script_path, "local_modules"), "setup.py")

    # Create a docs folder in the current directory
    docs_folder_path = os.path.join(script_path, "docs")

    try:
        # Remove the folder if it exists
        shutil.rmtree(docs_folder_path)
        logger(f"Folder '{docs_folder_path}' removed successfully.")
    except FileNotFoundError:
        logger(f"Folder '{docs_folder_path}' not found.", "warn")
    except Exception as e:
        logger(f"An error occurred: {str(e)}", "critical")
    os.mkdir(docs_folder_path)
    os.mkdir(os.path.join(docs_folder_path, "source"))
    logger(f"Created 'docs' folder in {script_path}")


def launch_sphinx_api(version_mip):
    """
    This function launches the sphinx API.

    :param version_mip: The version of the MIP.

    :return: None
    """
    docs_folder_path = os.path.join(script_path, "docs")
    print(docs_folder_path)
    os.chdir(docs_folder_path)
    # Run the 'sphinx-quickstart' command
    try:
        log_and_process(
            [
                "sphinx-quickstart",
                "--sep",
                "-d",
                os.path.join(docs_folder_path, "source"),
                "-q",
                "-p",
                "Project Reloaded",
                "-a",
                "Project",
                "-v",
                version_mip,
                "-r",
                version_mip,
                "-l",
                "en",
                ".",
            ]
        )
    except Exception as e:
        logger(f"Error while generating documentation: {e}", "error")
        logger(e, "critical")

    os.chdir(script_path)
    try:
        log_and_process(
            ["sphinx-apidoc", "-e", "-d", "1", "-o", "docs/source", "local_modules/."]
        )
        logger("Documentation generated successfully")
    except Exception as e:
        logger(f"Error while generating documentation: {e}", "error")
        logger(e, "critical")

    copy_file(
        os.path.join(script_path, "assets", "source", "conf.py"),
        os.path.join(docs_folder_path, "source", "conf.py"),
    )

    copy_file(
        os.path.join(script_path, "assets", "source", "index.rst"),
        os.path.join(docs_folder_path, "source", "index.rst"),
    )

    copy_file(
        os.path.join(script_path, "assets", "templates", "layout.html"),
        os.path.join(docs_folder_path, "source", "_templates", "layout.html"),
    )

    copy_file(
        os.path.join(script_path, "assets", "templates", "module.rst"),
        os.path.join(docs_folder_path, "source", "_templates", "module.rst"),
    )

    copy_file(
        os.path.join(script_path, "assets", "static", "my_theme.css"),
        os.path.join(docs_folder_path, "source", "_static", "my_theme.css"),
    )

    copy_file(
        os.path.join(script_path, "assets", "static", "logo.png"),
        os.path.join(docs_folder_path, "source", "_static", "logo.png"),
    )

    change_version(
        os.path.join(docs_folder_path, "source", "conf.py"),
        version_mip,
    )

    log_and_process(
        [
            "sphinx-build",
            "-b",
            "html",
            os.path.join(docs_folder_path, "source"),
            os.path.join(docs_folder_path, "build"),
        ]
    )


def create_zip_file_sphinx_build(password, self_progress):
    """
    This function creates a ZIP file with password protection.

    :param password: The password to use for the ZIP file

    :param self_progress: The progress bar to update.

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
        script_path, "builds", f"build_{formatted_datetime}.zip"
    )

    self_progress.set(0)
    total_files = sum(len(filenames) for _, _, filenames in os.walk(source_directory))
    step = 1 / total_files
    nb_files_treated = 0
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
                    nb_files_treated += 1
                    self_progress.set(nb_files_treated * step)

        # Add a password to the ZIP file
        zipf.setpassword(bytes(password, "utf-8"))
        logger(f'ZIP file "{destination_directory}" created with password protection.')
        return destination_directory, os.path.join(script_path, "builds")
    except Exception as e:
        logger(f"An error occurred: {str(e)}", "critical")
