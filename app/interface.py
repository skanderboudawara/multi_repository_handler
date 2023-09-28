import datetime
import os
import tkinter as tk

import customtkinter as ctk
from app.logger import logger
from app.up.add_repository_popup import AddRepository
from app.up.branch_commit_popup import CommitRepository
from app.up.branch_creator_popup import AddBranchToAllRepositories
from app.up.repo_updater_popup import UpdateRepositories
from app.up.show_repo_popup import ShowActifRepositories
from app.up.sphinx_creator_popup import SphinxCreatorPopup
from app.utils import scan_all_repositories

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


class MultiRepoManager(ctk.CTk):
    # Function to add a repository
    """
    This class is used to create the main window of the application

    :param: None

    :returns: None
    """

    def __init__(self) -> None:
        # Create the main Tkinter window
        # Set the appearance mode to 'dark'
        super().__init__()
        scan_all_repositories()

        logger(f"🔄 New session created at {str(datetime.datetime.now())}")
        logger(f"local path: {script_path}")

        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")

        self.title("Multi Repository Handler")
        self.geometry("420x350")
        self.resizable(False, False)
        self.add_repository_popup = None
        self.branch_commit_popup = None
        self.branch_creator_popup = None
        self.repo_updater_popup = None
        self.show_repo_popup = None
        self.sphinx_creator_popup = None

        ctk.CTkLabel(
            self,
            text="Multi Repository Handler",
            font=("Helvetica", 16, "bold"),
            anchor="center",
        ).pack(pady=5, ipady=5)
        self.main_window()

    def run(self) -> None:
        """
        This method is used to run the application

        :param: None

        :returns: None
        """
        self.mainloop()

    def open_add_repository_popup(self):
        if (
            self.add_repository_popup is None
            or not self.add_repository_popup.winfo_exists()
        ):
            self.withdraw()
            self.add_repository_popup = AddRepository(self)
        else:
            self.add_repository_popup.focus()

    def open_repo_updater_popup(self):
        if (
            self.repo_updater_popup is None
            or not self.repo_updater_popup.winfo_exists()
        ):
            self.withdraw()
            self.repo_updater_popup = UpdateRepositories(self)
        else:
            self.repo_updater_popup.focus()

    def open_branch_creator_popup(self):
        if (
            self.branch_creator_popup is None
            or not self.branch_creator_popup.winfo_exists()
        ):
            self.withdraw()
            self.branch_creator_popup = AddBranchToAllRepositories(self)
        else:
            self.branch_creator_popup.focus()

    def open_branch_commit_popup(self):
        if (
            self.branch_commit_popup is None
            or not self.branch_commit_popup.winfo_exists()
        ):
            self.withdraw()
            self.branch_commit_popup = CommitRepository(self)
        else:
            self.branch_commit_popup.focus()

    def open_show_repo_popup(self):
        if self.show_repo_popup is None or not self.show_repo_popup.winfo_exists():
            self.withdraw()
            self.show_repo_popup = ShowActifRepositories(self)
        else:
            self.show_repo_popup.focus()

    def open_sphinx_creator_popup(self):
        if (
            self.sphinx_creator_popup is None
            or not self.sphinx_creator_popup.winfo_exists()
        ):
            self.withdraw()
            self.sphinx_creator_popup = SphinxCreatorPopup(self)
        else:
            self.sphinx_creator_popup.focus()

    def main_window(self):
        """
        This method is used to create the main window of the application

        :param: None

        :returns: None
        """

        frame = ctk.CTkFrame(self, width=400, height=400, corner_radius=10)
        frame.pack(pady=10)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        add_button = ctk.CTkButton(
            frame,
            text="Add\nRepository",
            width=150,
            height=70,
            command=self.open_add_repository_popup,
            font=("Inter", 15),
            corner_radius=10,
        )

        add_button.grid(row=2, column=1, padx=10, pady=10)

        update_button = ctk.CTkButton(
            frame,
            text="Update & Checkout\nLocal Repositories",
            width=150,
            height=70,
            command=self.open_repo_updater_popup,
            font=("Inter", 15),
            corner_radius=10,
        )

        update_button.grid(row=2, column=2, padx=20, pady=10)

        create_new_branch = ctk.CTkButton(
            frame,
            text="Create branch\nin all repos",
            width=150,
            height=70,
            command=self.open_branch_creator_popup,
            font=("Inter", 15),
            corner_radius=10,
        )

        create_new_branch.grid(row=3, column=1, padx=10, pady=10)

        commit_to_all_btn = ctk.CTkButton(
            frame,
            text="Commit to all\n repositories",
            width=150,
            height=70,
            command=self.open_branch_commit_popup,
            font=("Inter", 15),
            corner_radius=10,
        )

        commit_to_all_btn.grid(row=3, column=2, padx=10, pady=10)

        show_active = ctk.CTkButton(
            frame,
            text="Show added\nrepositories",
            width=150,
            height=70,
            command=self.open_show_repo_popup,
            font=("Inter", 15),
            corner_radius=10,
        )

        show_active.grid(row=4, column=1, padx=10, pady=10)

        create_sphinx_doc = ctk.CTkButton(
            frame,
            text="Create Sphinx\nDocumentation",
            width=150,
            height=70,
            command=self.open_sphinx_creator_popup,
            font=("Inter", 15),
            corner_radius=10,
        )

        create_sphinx_doc.grid(row=4, column=2, padx=10, pady=10)

    def show_alert(self, message):
        """
        This function shows an alert message.

        :param message: The message to show

        :return: None
        """
        tk.messagebox.showinfo("Info", message)
