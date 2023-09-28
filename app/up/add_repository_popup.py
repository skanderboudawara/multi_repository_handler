import json
import os
import threading

import customtkinter as ctk
from app.logger import logger
from app.utils import clone_repository_git, get_json_data

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\..")


class AddRepository(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(master=root)
        logger("Add repository")
        self.root = root
        self.after(100, self.lift)
        self.title("Add Repository")
        self.geometry("600x130")
        self.protocol("WM_DELETE_WINDOW", self.close_popup)

        ctk.CTkLabel(self, text="Enter Repository URL:").pack(pady=5)
        self.repo_entry = ctk.CTkEntry(self, width=550, height=30)
        self.repo_entry.pack(pady=5)

        thread_perform_add = threading.Thread(target=self.perform_add)
        self.button_add = ctk.CTkButton(
            self, text="Add", command=lambda: thread_perform_add.start()
        )
        self.button_add.pack(pady=5)

    def close_popup(self):
        self.root.deiconify()
        self.destroy()
        logger("Add repository Destroyed")

    def perform_add(self) -> None:
        """
        This method is used to add a repository to the application

        :param: None

        :returns: None
        """
        if repo_url := self.repo_entry.get():
            self.button_add.configure(state="disabled")
            self.repo_entry.configure(state="disabled")
            # Extract the repository name from the URL
            repo_name = repo_url.split("/")[-1]

            # Check if repo_name contains ".git" and remove it
            if ".git" in repo_name:
                repo_name = repo_name.replace(".git", "")

            # Ensure 'remote_repositories' folder exists
            os.makedirs("remote_repositories", exist_ok=True)

            # Clone the repository into the 'remote_repositories' folder
            clone_folder = os.path.join(script_path, "remote_repositories")
            os.chdir(clone_folder)

            try:
                clone_repository_git(repo_url, clone_folder)
            except Exception as e:
                logger(f"{e} local repo already exists {repo_name}", "warn")

            os.chdir(script_path)
            # Add repository data to JSON file

            repos_data, f_repo_json = get_json_data()

            logger(f"The repo {repo_name} have been added!")
            repos_data[repo_name] = repo_url
            with open(f_repo_json, "w") as json_file:
                json.dump(repos_data, json_file, indent=4)

            self.close_popup()
            self.root.show_alert("Repository added successfully!")
        else:
            self.close_popup()
            self.root.show_alert("Please add a non empty repository URL!")
            return