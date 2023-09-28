import os
import threading

import customtkinter as ctk
from app.logger import logger
from app.utils import create_branch_if_not_exist, get_json_data

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\..")


class AddBranchToAllRepositories(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(master=root)
        logger("Add Branch to all repositories")
        self.root = root
        self.after(100, self.lift)
        self.title("Branch creator")
        self.geometry("300x220")
        self.protocol("WM_DELETE_WINDOW", self.close_popup)

        ctk.CTkLabel(self, text="Enter The base branch (from):").pack(pady=5)

        self.from_branch = ctk.CTkEntry(self, width=250, height=30)
        self.from_branch.pack(pady=5)

        ctk.CTkLabel(self, text="Enter The branch name you want to deploy").pack(pady=5)

        self.new_branch = ctk.CTkEntry(self, width=250, height=30)
        self.new_branch.pack(pady=5)

        self.thread_add_repo = threading.Thread(target=self.add_to_all_repos)
        self.add_button = ctk.CTkButton(
            self,
            width=100, height=25,
            text="Create branch in all repositories",
            command=lambda: self.thread_add_repo.start(),
        )
        self.add_button.pack(pady=5)

        

    def close_popup(self):
        """
        This method is used to close the pop-up dialog

        :param: None

        :returns: None
        """
        self.destroy()
        self.root.deiconify()

    def add_to_all_repos(self) -> None:
        """
        This method is used to create a new branch in all local repositories

        :param: None

        :returns: None
        """
        from_branch_name = self.from_branch.get()
        new_branch_name = self.new_branch.get()
        if not from_branch_name:
            self.close_popup()
            self.root.show_alert("Please enter a name of a base branch!")
            return
        if not new_branch_name:
            self.close_popup()
            self.root.show_alert("Please enter a name of a new branch!")
            return
        if new_branch_name == from_branch_name:
            self.close_popup()
            self.root.show_alert("Please enter a different name for the new branch!")
            return
        logger(
            f"Create branch {new_branch_name} in all local repositories \
                from {from_branch_name}"
        )
        repos_data, _ = get_json_data()

        if repos_data:
            self.add_button.configure(
                width=100, height=25,
                state="disabled"
            )
            self.from_branch.configure(state="disabled")
            self.new_branch.configure(state="disabled")

            all_repositories = list(repos_data.keys())
            root_directory = os.path.join(script_path, "remote_repositories")

            # Create a progress bar
            self.geometry("300x270")
            self.labled_add_progress = ctk.CTkLabel(self, text="Adding branch to all repos")
            self.progress_bar_adding_to_all = ctk.CTkProgressBar(
                self,
                width=250,
            )
            self.labled_add_progress.pack(pady=5)
            self.progress_bar_adding_to_all.pack(pady=5)
            self.progress_bar_adding_to_all.set(0)

            try:
                create_branch_if_not_exist(
                    root_directory,
                    all_repositories,
                    new_branch_name,
                    from_branch_name,  # Base branch example "dev"
                    self.progress_bar_adding_to_all,
                )
                logger(
                    f"All repositories have been updated with \
                        the new branch {new_branch_name}!"
                )
            except Exception as e:
                logger(
                    f"Failed to create new branch {new_branch_name} \
                        in all repositories!",
                    "error",
                )
                logger(e, "critical")

            self.progress_bar_adding_to_all.configure(progress_color="green")
            self.close_popup()
            self.root.show_alert("A new branch has been created in all repositories!")
