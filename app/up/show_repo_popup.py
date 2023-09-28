import json
import os

import customtkinter as ctk
from app.logger import logger
from app.utils import get_json_data, remove_directory_if_exists

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\..")


class ShowActifRepositories(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(master=root)
        logger("Show active repositories")
        self.root = root
        self.after(100, self.lift)
        self.title("Branch creator")
        self.geometry("315x400")
        self.protocol("WM_DELETE_WINDOW", self.close_popup)

        # Create and pack widgets in the pop-up dialog
        ctk.CTkLabel(self, text="All active repositories:").grid(row=0, column=0)

        self.update_frame()

        ctk.CTkButton(
            self,
            text="Close",
            command=self.close_popup,
        ).grid(row=2, column=0)

    def remove_selected(self, repo_name: str, data: dict, json_file: str) -> None:
        remove_directory_if_exists(
            os.path.join(script_path, "local_modules", repo_name)
        )
        remove_directory_if_exists(
            os.path.join(script_path, "remote_repositories", repo_name)
        )

        if repo_name in data:
            del data[repo_name]
            logger(f"Removed key '{repo_name}' from the JSON data.")

        # Save the updated JSON back to the file
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)

        logger("JSON file updated successfully.")

        self.root.show_alert("Repository removed successfully!")
        self.frame_repos.destroy()
        self.update_frame()

    def update_frame(self):
        """
        This method is used to update the frame of the pop-up dialog

        :param: None

        :returns: None
        """
        self.frame_repos = ctk.CTkScrollableFrame(self, width=270, height=250)
        self.frame_repos.grid(row=1, column=0, padx=10, pady=10)
        self.frame_repos.columnconfigure(0, weight=1)
        self.frame_repos.columnconfigure(1, weight=3)
        repos_data, f_repo_json = get_json_data()

        if repos_data:
            for i, repo_name in enumerate(repos_data.keys()):
                ctk.CTkButton(
                    self.frame_repos,
                    text="Remove",
                    command=lambda: self.remove_selected(
                        repo_name, repos_data, f_repo_json
                    ),
                    width=14,
                ).grid(row=i, column=0, padx=20, sticky="e", pady=5)
                ctk.CTkLabel(
                    self.frame_repos, anchor="w", text=repo_name, wraplength=120
                ).grid(row=i, column=1, padx=20, sticky="w", pady=5)

    def close_popup(self):
        """
        This method is used to close the pop-up dialog

        :param: None

        :returns: None
        """
        self.root.deiconify()
        self.destroy()
