import os
import shutil

from app.logger import logger
from app.utils import (change_version, copy_file, copy_modules,
                       create_zip_file, log_and_process, remove_file_batch)

script_path = os.getcwd()
print(script_path)


def generate_documentation(all_repositories, version_mip, password):
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

    path_zip = create_zip_file(password)

    return path_zip
