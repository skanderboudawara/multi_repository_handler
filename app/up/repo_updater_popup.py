import os
import threading

import customtkinter as ctk
from app.logger import logger
from app.utils import get_json_data, update_all_local_repositories

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\..")


class UpdateRepositories(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(master=root)
        logger("Update repositories")
        self.root = root
        self.after(100, self.lift)
        self.title("Update repositories")
        self.geometry("300x150")
        self.protocol("WM_DELETE_WINDOW", self.close_popup)

        # Create and pack widgets in the pop-up dialog
        ctk.CTkLabel(self, text="Enter The branch to checkout to:").pack(pady=5)

        self.branch_entry = ctk.CTkEntry(self, width=250, height=30)
        self.branch_entry.pack(pady=5)

        self.labled_update = ctk.CTkLabel(self, text="Updating all repositories")
        self.progress_bar_update = ctk.CTkProgressBar(self, width=250)

        thread_perform_update = threading.Thread(target=self.perform_update)
        self.add_button = ctk.CTkButton(
            self,
            text="Update all repositories",
            command=lambda: thread_perform_update.start(),
        )
        self.add_button.pack(pady=5)

    def close_popup(self):
        """
        This method is used to close the pop-up dialog

        :param: None

        :returns: None
        """
        self.root.deiconify()
        self.destroy()

    def perform_update(self) -> None:
        """
        This method is used to update all local repositories

        :param: None

        :returns: None
        """
        if repo_branch := self.branch_entry.get():
            logger(f"Update all local repositories to {repo_branch}")
            repos_data, _ = get_json_data()

            if repos_data:
                self.add_button.configure(state="disabled")
                self.branch_entry.configure(state="disabled")

                all_repositories = list(repos_data.keys())
                root_directory = os.path.join(script_path, "remote_repositories")

                # Create a progress bar
                self.geometry("300x200")
                self.labled_update.pack(pady=5)
                self.progress_bar_update.pack(pady=5)
                self.progress_bar_update.set(0)

                try:
                    update_all_local_repositories(
                        root_directory,
                        all_repositories,
                        repo_branch,
                        self.progress_bar_update,
                    )
                    logger("All repositories have been updated!")
                except Exception as e:
                    logger("Failed to update all repositories!", "error")
                    logger(e, "critical")

                self.progress_bar_update.configure(progress_color="green")
                self.close_popup()
                self.root.show_alert("All repositories have been updated!")
        else:
            self.close_popup()
            self.root.show_alert("Please enter a name of a branch!")
            return
