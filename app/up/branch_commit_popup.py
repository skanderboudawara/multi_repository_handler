import os
import threading

import customtkinter as ctk
from app.logger import logger
from app.utils import commit_push, get_json_data

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\..")


class CommitRepository(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(master=root)
        logger("Commit repos")
        self.root = root
        self.after(100, self.lift)
        self.title("Commit manager")
        self.geometry("300x220")
        self.protocol("WM_DELETE_WINDOW", self.close_popup)

        # Create and pack widgets in the pop-up dialog
        ctk.CTkLabel(self, text="Enter The commit message:").pack(pady=5)

        self.commit_message = ctk.CTkEntry(self, width=250, height=30)
        self.commit_message.pack(pady=5)

        ctk.CTkLabel(self, text="Enter The branch name for commit").pack(pady=5)

        self.branch_for_commit = ctk.CTkEntry(self, width=250, height=30)
        self.branch_for_commit.pack(pady=5)

        self.labled_add_commit = ctk.CTkLabel(self, text="Commit all branches")
        self.progress_bar_add_commit = ctk.CTkProgressBar(self, width=250)

        thread_commit_to_all_repo = threading.Thread(target=self.commit_to_all_repo)
        self.add_button = ctk.CTkButton(
            self,
            width=100, height=25,
            text="Commit to all repositories",
            command=lambda: thread_commit_to_all_repo.start(),
        )
        self.add_button.pack(pady=5)

    def close_popup(self):
        self.root.deiconify()
        self.destroy()
        logger("Commit manager Destroyed")

    def commit_to_all_repo(self) -> None:
        """
        This method is used to create a new branch in all local repositories

        :param: None

        :returns: None
        """
        commit_message_name = self.commit_message.get()
        branch_for_commit_name = self.branch_for_commit.get()
        if not commit_message_name:
            self.root.show_alert("Please enter a commit message!")
            self.close_popup()
            return
        if not branch_for_commit_name:
            self.root.show_alert("Please enter a branch name!")
            self.close_popup()
            return
        if commit_message_name == branch_for_commit_name:
            self.root.show_alert(
                "Please enter a different commit message and branch name!"
            )
            self.close_popup()
            return

        logger(
            f"Create branch {branch_for_commit_name} in all local repositories "
            f"from {commit_message_name}"
        )
        if branch_for_commit_name and commit_message_name:

            self.geometry("300x270")
            self.labled_add_commit.pack(pady=5)
            self.progress_bar_add_commit.pack(pady=5)
            self.progress_bar_add_commit.set(0)

            repos_data, _ = get_json_data()

            if repos_data:
                self.add_button.configure(
                    width=100, height=25,
                    state="disabled",
                )
                self.commit_message.configure(state="disabled")
                self.branch_for_commit.configure(state="disabled")

                all_repositories = repos_data.keys()

                try:
                    commit_push(
                        all_repositories,
                        branch_for_commit_name,
                        commit_message_name,
                        self.progress_bar_add_commit,
                    )
                    logger(
                        f"All repositories have been updated with the new branch "
                        f"{branch_for_commit_name}! with the commit message "
                        f"{commit_message_name}"
                    )
                except Exception as e:
                    logger("Failed to commit to all repositories!", "error")
                    logger(e, "critical")

                self.progress_bar_add_commit.configure(progress_color="green")
                self.close_popup()
                self.root.show_alert("A new commit has been created in all repositories!")
