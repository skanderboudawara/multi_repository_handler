"""
This module is used to create the main window of the application
"""
import datetime
import json
import os
import platform

import customtkinter as ctk
from app.generate_documentation import generate_documentation
from app.logger import logger
from app.utils import (
    clone_repository_git,
    commit_push,
    create_branch_if_not_exist,
    remove_directory_if_exists,
    scan_all_repositories,
    update_all_local_repositories,
)

script_path = os.getcwd()
print(script_path)


class MultiRepoManager:
    # Function to add a repository
    """
    This class is used to create the main window of the application

    :param: None

    :returns: None
    """

    def __init__(self) -> None:
        # Create the main Tkinter window
        # Set the appearance mode to 'dark'
        scan_all_repositories()
        logger("🔄 New session created at " + str(datetime.datetime.now()))
        logger("local path: " + script_path)
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")
        self.f_repo_json = os.path.join(script_path, "app/repos.json")
        self.root = ctk.CTk()
        self.root.title("Multi Repository Handler")
        # self.root.iconbitmap("assets/logo.ico")
        self.root.geometry("420x350")
        self.root.resizable(False, False)
        self.main_window()

    def run(self) -> None:
        """
        This method is used to run the application

        :param: None

        :returns: None
        """
        self.root.mainloop()

    def main_window(self):
        """
        This method is used to create the main window of the application

        :param: None

        :returns: None
        """
        widget_title = ctk.CTkLabel(
            self.root,
            text="Multi Repository Handler",
            font=("Helvetica", 16, "bold"),
            anchor="center",
        )
        widget_title.pack(pady=5, ipady=5)

        frame = ctk.CTkFrame(self.root, width=400, height=400, corner_radius=10)
        frame.pack(pady=10)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        add_button = ctk.CTkButton(
            frame,
            text="Add\nRepository",
            width=150,
            height=70,
            command=self.add_repository,
            font=("Inter", 15),
            corner_radius=10,
        )

        add_button.grid(row=2, column=1, padx=10, pady=10)

        update_button = ctk.CTkButton(
            frame,
            text="Update & Checkout\nLocal Repositories",
            width=150,
            height=70,
            command=self.update_repository,
            font=("Inter", 15),
            corner_radius=10,
        )

        update_button.grid(row=2, column=2, padx=20, pady=10)

        create_new_branch = ctk.CTkButton(
            frame,
            text="Create branch\nin all repos",
            width=150,
            height=70,
            command=self.add_to_all_repository,
            font=("Inter", 15),
            corner_radius=10,
        )

        create_new_branch.grid(row=3, column=1, padx=10, pady=10)

        commit_to_all_btn = ctk.CTkButton(
            frame,
            text="Commit to all\n repositories",
            width=150,
            height=70,
            command=self.commit_to_all_branches,
            font=("Inter", 15),
            corner_radius=10,
        )

        commit_to_all_btn.grid(row=3, column=2, padx=10, pady=10)

        show_active = ctk.CTkButton(
            frame,
            text="Show added\nrepositories",
            width=150,
            height=70,
            command=self.show_active_repositories,
            font=("Inter", 15),
            corner_radius=10,
        )

        show_active.grid(row=4, column=1, padx=10, pady=10)

        create_sphinx_doc = ctk.CTkButton(
            frame,
            text="Create Sphinx\nDocumentation",
            width=150,
            height=70,
            command=self.create_sphinx_documentation,
            font=("Inter", 15),
            corner_radius=10,
        )

        create_sphinx_doc.grid(row=4, column=2, padx=10, pady=10)

    def add_repository(self) -> None:
        """
        This method is used to add a repository to the application

        :param: None

        :returns: None
        """
        logger("Add repository")
        # Create a new top-level window for the pop-up dialog
        self.root.withdraw()
        popup_add = ctk.CTkToplevel(self.root)
        popup_add.after(100, popup_add.lift)
        popup_add.title("Add Repository")
        popup_add.geometry("600x130")

        def close_popup():
            self.root.deiconify()
            popup_add.destroy()

        popup_add.protocol("WM_DELETE_WINDOW", close_popup)

        # Create and pack widgets in the pop-up dialog
        label = ctk.CTkLabel(popup_add, text="Enter Repository URL:")
        label.pack(pady=5)

        repo_entry = ctk.CTkEntry(
            popup_add,
            width=550,
            height=30,
        )
        repo_entry.pack(pady=5)

        def perform_add() -> None:
            """
            This method is used to add a repository to the application

            :param: None

            :returns: None
            """
            repo_url = repo_entry.get()
            if repo_url:
                # Extract the repository name from the URL
                repo_name = repo_url.split("/")[-1]

                # Check if repo_name contains ".git" and remove it
                if ".git" in repo_name:
                    repo_name = repo_name.replace(".git", "")

                # Ensure 'remote_repositories' folder exists
                os.makedirs("remote_repositories", exist_ok=True)

                # Clone the repository into the 'remote_repositories' folder
                clone_folder = os.path.join(script_path, "remote_repositories")
                print(clone_folder)
                os.chdir(clone_folder)

                try:
                    clone_repository_git(repo_url, clone_folder)
                except Exception as e:
                    logger(f"{e} local repo already exists {repo_name}", "warn")

                os.chdir(script_path)
                # Add repository data to JSON file

                try:
                    with open(self.f_repo_json, "r") as json_file:
                        repos_data = json.load(json_file)
                except FileNotFoundError:
                    repos_data = {}
                    logger("No repos.json file found, creating a new one", "warn")
                logger(f"The repo {repo_name} have been added!")
                repos_data[repo_name] = repo_url
                with open(self.f_repo_json, "w") as json_file:
                    json.dump(repos_data, json_file, indent=4)

                close_popup()

        add_button = ctk.CTkButton(popup_add, text="Add", command=perform_add)
        add_button.pack(pady=5)

    def update_repository(self) -> None:
        """
        This method is used to update all local repositories

        :param: None

        :returns: None
        """
        # Create a new top-level window for the pop-up dialog

        self.root.withdraw()
        popup_update = ctk.CTkToplevel(self.root)
        popup_update.after(100, popup_update.lift)
        popup_update.title("Update repository")
        popup_update.geometry("300x150")

        def close_popup():
            self.root.deiconify()
            popup_update.destroy()

        popup_update.protocol("WM_DELETE_WINDOW", close_popup)

        # Create and pack widgets in the pop-up dialog
        label = ctk.CTkLabel(popup_update, text="Enter The branch to checkout to:")
        label.pack(pady=5)

        branch_entry = ctk.CTkEntry(
            popup_update,
            width=250,
            height=30,
        )
        branch_entry.pack(pady=5)

        def perform_update() -> None:
            """
            This method is used to update all local repositories

            :param: None

            :returns: None
            """
            repo_branch = branch_entry.get()
            if repo_branch:
                logger(f"Update all local repositories to {repo_branch}")

                try:
                    with open(self.f_repo_json, "r") as json_file:
                        repos_data = json.load(json_file)
                except FileNotFoundError:
                    repos_data = None

                if repos_data:
                    add_button.configure(state="disabled")
                    branch_entry.configure(state="disabled")

                    all_repositories = list(repos_data.keys())
                    root_directory = os.path.join(script_path, "remote_repositories")

                    # Create a progress bar
                    progress_bar = ctk.CTkLabel(
                        popup_update,
                        text="Updating all repositories...",
                    )
                    progress_bar.pack(pady=5)

                    try:
                        update_all_local_repositories(
                            root_directory,
                            all_repositories,
                            repo_branch,
                        )
                        logger("All repositories have been updated!")
                    except Exception as e:
                        logger("Failed to update all repositories!", "error")
                        logger(e, "critical")

                    progress_bar.configure(text="All repositories have been updated!")

                    close_popup()

        add_button = ctk.CTkButton(
            popup_update, text="Update all repositories", command=perform_update
        )
        add_button.pack(pady=5)

    def add_to_all_repository(self) -> None:
        """
        This method is used to create a new branch in all local repositories

        :param: None

        :returns: None
        """
        # Create a new top-level window for the pop-up dialog
        self.root.withdraw()
        add_to_all_repositories = ctk.CTkToplevel(self.root)
        add_to_all_repositories.after(100, add_to_all_repositories.lift)
        add_to_all_repositories.title("Branch creator")
        add_to_all_repositories.geometry("300x220")

        def close_popup():
            self.root.deiconify()
            add_to_all_repositories.destroy()

        add_to_all_repositories.protocol("WM_DELETE_WINDOW", close_popup)

        # Create and pack widgets in the pop-up dialog
        label = ctk.CTkLabel(
            add_to_all_repositories, text="Enter The base branch (from):"
        )
        label.pack(pady=5)

        from_branch = ctk.CTkEntry(
            add_to_all_repositories,
            width=250,
            height=30,
        )
        from_branch.pack(pady=5)

        label = ctk.CTkLabel(
            add_to_all_repositories, text="Enter The branch name you want to deploy"
        )
        label.pack(pady=5)

        new_branch = ctk.CTkEntry(
            add_to_all_repositories,
            width=250,
            height=30,
        )
        new_branch.pack(pady=5)

        def add_to_all_repos() -> None:
            """
            This method is used to create a new branch in all local repositories

            :param: None

            :returns: None
            """
            from_branch_name = from_branch.get()
            new_branch_name = new_branch.get()
            if from_branch and new_branch:
                logger(
                    f"Create branch {new_branch_name} in all local repositories from {from_branch_name}"
                )

                try:
                    with open(self.f_repo_json, "r") as json_file:
                        repos_data = json.load(json_file)
                except FileNotFoundError:
                    repos_data = None

                if repos_data:
                    add_button.configure(state="disabled")
                    from_branch.configure(state="disabled")
                    new_branch.configure(state="disabled")

                    all_repositories = list(repos_data.keys())
                    root_directory = os.path.join(script_path, "remote_repositories")

                    # Create a progress bar
                    progress_bar = ctk.CTkLabel(
                        add_to_all_repositories,
                        text="Adding new branch to all repositories...",
                    )
                    progress_bar.pack(pady=5)

                    try:
                        create_branch_if_not_exist(
                            root_directory,
                            all_repositories,
                            new_branch_name,
                            from_branch_name,  # Base branch example "dev"
                        )
                        logger(
                            f"All repositories have been updated with the new branch {new_branch_name}!"
                        )
                    except Exception as e:
                        logger(
                            f"Failed to create new branch {new_branch_name} in all repositories!",
                            "error",
                        )
                        logger(e, "critical")

                    close_popup()

        add_button = ctk.CTkButton(
            add_to_all_repositories,
            text="Create branch in all repositories",
            command=add_to_all_repos,
        )
        add_button.pack(pady=5)

    def show_active_repositories(self) -> None:
        """
        This method is used to create a new branch in all local repositories

        :param: None

        :returns: None
        """
        # Create a new top-level window for the pop-up dialog
        self.root.withdraw()
        show_repositories = ctk.CTkToplevel(self.root)
        show_repositories.after(100, show_repositories.lift)
        show_repositories.title("Branch creator")
        show_repositories.geometry("315x400")

        def close_popup():
            self.root.deiconify()
            show_repositories.destroy()

        show_repositories.protocol("WM_DELETE_WINDOW", close_popup)

        # Create and pack widgets in the pop-up dialog
        label = ctk.CTkLabel(show_repositories, text="All active repositories:")
        label.grid(row=0, column=0)

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

            self.frame_repos.destroy()
            update_frame(self)

        def update_frame(self):
            repos_data = None
            try:
                with open(self.f_repo_json, "r") as json_file:
                    repos_data = json.load(json_file)
            except FileNotFoundError:
                logger("No repos.json file found, creating a new one", "warn")

            if repos_data:
                self.frame_repos = ctk.CTkScrollableFrame(
                    show_repositories,
                    width=270,
                    height=250,
                )
                self.frame_repos.grid(row=1, column=0, padx=10, pady=10)
                # self.frame_repos.grid_columnconfigure(2, weight=2)

                for i, repo_name in enumerate(repos_data.keys()):
                    close_button = ctk.CTkButton(
                        self.frame_repos,
                        text="Remove",
                        # text="🗑️",
                        command=lambda: remove_selected(
                            self, repo_name, repos_data, self.f_repo_json
                        ),
                        width=14,
                    )
                    close_button.grid(row=i, column=0, padx=20, sticky="e", pady=5)
                    label = ctk.CTkLabel(
                        self.frame_repos, anchor="e", text=repo_name, wraplength=150
                    )
                    label.grid(row=i, column=1, padx=20, sticky="w", pady=5)

        update_frame(self)

        close_button = ctk.CTkButton(
            show_repositories,
            text="Close",
            command=close_popup,
        )
        close_button.grid(row=2, column=0)

    def create_sphinx_documentation(self) -> None:
        """
        This method is used to create documentation for all local repositories

        :param: None

        :returns: None
        """
        # Create a new top-level window for the pop-up dialog
        self.root.withdraw()
        create_doc_popup = ctk.CTkToplevel(self.root)
        create_doc_popup.after(100, create_doc_popup.lift)
        create_doc_popup.title("Create sphinx documentation")
        create_doc_popup.geometry("300x220")

        def close_popup():
            self.root.deiconify()
            create_doc_popup.destroy()

        create_doc_popup.protocol("WM_DELETE_WINDOW", close_popup)

        # Create and pack widgets in the pop-up dialog
        label = ctk.CTkLabel(create_doc_popup, text="Enter the MIP Version")
        label.pack(pady=5)

        mip_version = ctk.CTkEntry(
            create_doc_popup,
            width=250,
            height=30,
        )
        mip_version.pack(pady=5)

        label = ctk.CTkLabel(create_doc_popup, text="Enter The Zip file password")
        label.pack(pady=5)

        zip_file_password = ctk.CTkEntry(
            create_doc_popup,
            width=250,
            height=30,
        )
        zip_file_password.pack(pady=5)

        def create_sphinx_doc() -> None:
            """
            This method is used to create a new branch in all local repositories

            :param: None

            :returns: None
            """
            mip_version_name = mip_version.get()
            zip_file_password_name = zip_file_password.get()
            if mip_version and zip_file_password:
                logger(
                    f"Create processing create sphinx documentation with {mip_version_name}"
                )

                try:
                    with open(self.f_repo_json, "r") as json_file:
                        repos_data = json.load(json_file)
                except FileNotFoundError:
                    repos_data = None

                if repos_data:
                    add_button.configure(state="disabled")
                    mip_version.configure(state="disabled")
                    zip_file_password.configure(state="disabled")

                    all_repositories = repos_data.keys()

                    # Create a progress bar
                    progress_bar = ctk.CTkLabel(
                        create_doc_popup,
                        text="Creating documentation please wait...",
                    )
                    progress_bar.pack(pady=5)

                    try:
                        file_zip, folder_path = generate_documentation(
                            all_repositories,
                            mip_version_name,
                            zip_file_password_name,
                        )

                        # Get the current system's platform
                        current_platform = platform.system()

                        if current_platform == "Windows":
                            os.system(f'explorer "{folder_path}"')
                        elif current_platform == "Darwin":  # macOS
                            os.system(f'open "{folder_path}"')
                        elif current_platform == "Linux":
                            os.system(f'xdg-open "{folder_path}"')
                        else:
                            logger(
                                f"Opening folders is not supported on the {current_platform} platform."
                            )
                        logger(
                            f"The zip file has been created successfully! {file_zip}"
                        )

                    except Exception as e:
                        logger(
                            "Failed to create the Zip file!",
                            "error",
                        )
                        logger(e, "critical")

                    close_popup()

        add_button = ctk.CTkButton(
            create_doc_popup,
            text="Create documentation",
            command=create_sphinx_doc,
        )
        add_button.pack(pady=5)

    def commit_to_all_branches(self) -> None:
        """
        This method is used to create a new branch in all local repositories

        :param: None

        :returns: None
        """
        # Create a new top-level window for the pop-up dialog
        self.root.withdraw()
        commit_to_all_popup = ctk.CTkToplevel(self.root)
        commit_to_all_popup.after(100, commit_to_all_popup.lift)
        commit_to_all_popup.title("Commit manager")
        commit_to_all_popup.geometry("300x220")

        def close_popup():
            self.root.deiconify()
            commit_to_all_popup.destroy()

        commit_to_all_popup.protocol("WM_DELETE_WINDOW", close_popup)

        # Create and pack widgets in the pop-up dialog
        label = ctk.CTkLabel(commit_to_all_popup, text="Enter The commit message:")
        label.pack(pady=5)

        commit_message = ctk.CTkEntry(
            commit_to_all_popup,
            width=250,
            height=30,
        )
        commit_message.pack(pady=5)

        label = ctk.CTkLabel(
            commit_to_all_popup, text="Enter The branch name for commit"
        )
        label.pack(pady=5)

        branch_for_commit = ctk.CTkEntry(
            commit_to_all_popup,
            width=250,
            height=30,
        )
        branch_for_commit.pack(pady=5)

        def commit_to_all_repo() -> None:
            """
            This method is used to create a new branch in all local repositories

            :param: None

            :returns: None
            """
            commit_message_name = commit_message.get()
            branch_for_commit_name = branch_for_commit.get()
            if commit_message and branch_for_commit:
                logger(
                    f"Create branch {branch_for_commit_name} in all local repositories from {commit_message_name}"
                )

                try:
                    with open(self.f_repo_json, "r") as json_file:
                        repos_data = json.load(json_file)
                except FileNotFoundError:
                    repos_data = None

                if repos_data:
                    add_button.configure(state="disabled")
                    commit_message.configure(state="disabled")
                    branch_for_commit.configure(state="disabled")

                    all_repositories = repos_data.keys()

                    # Create a progress bar
                    progress_bar = ctk.CTkLabel(
                        commit_to_all_popup,
                        text="Commit message...",
                    )
                    progress_bar.pack(pady=5)

                    try:
                        commit_push(
                            all_repositories,
                            branch_for_commit_name,
                            commit_message_name,
                        )
                        logger(
                            f"All repositories have been updated with the new branch {branch_for_commit_name}! with the commit message {commit_message_name}"
                        )
                    except Exception as e:
                        logger(
                            "Failed to commit to all repositories!",
                            "error",
                        )
                        logger(e, "critical")

                    close_popup()

        add_button = ctk.CTkButton(
            commit_to_all_popup,
            text="Commit to all repositories",
            command=commit_to_all_repo,
        )
        add_button.pack(pady=5)
