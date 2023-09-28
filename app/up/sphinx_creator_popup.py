import os
import platform
import shutil
import threading

import customtkinter as ctk
from app.generate_documentation import (create_zip_file_sphinx_build,
                                        launch_sphinx_api,
                                        preparing_files_and_folders_sphinx)
from app.logger import logger
from app.utils import count_files, get_json_data, thread_with_trace

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\..")


class SphinxCreatorPopup(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(master=root)
        logger("Create sphinx documentation")
        self.root = root
        self.after(100, self.lift)
        self.title("Create sphinx documentation")
        self.geometry("300x220")
        self.protocol("WM_DELETE_WINDOW", self.close_popup)

        # Create and pack widgets in the pop-up dialog
        ctk.CTkLabel(self, text="Enter the MIP Version").pack(pady=5)
        self.mip_version = ctk.CTkEntry(self, width=250, height=30)
        self.mip_version.pack(pady=5)

        ctk.CTkLabel(self, text="Enter The Zip file password").pack(pady=5)

        self.zip_file_password = ctk.CTkEntry(self, width=250, height=30)
        self.zip_file_password.pack(pady=5)

        thread_sphinx_doc = threading.Thread(target=self.create_sphinx_doc)
        self.add_button = ctk.CTkButton(
            self,
            text="Create documentation",
            command=lambda: thread_sphinx_doc.start(),
        )
        self.add_button.pack(pady=5)
        
        

    def close_popup(self):
        self.root.deiconify()
        self.destroy()
        logger("Add repository Destroyed")

    def create_progress_bar(self) -> None:
        """
        THis method is used to create the progress bar

        :param: None

        :returns: None
        """
        self.geometry("300x330")
        self.progress_frame = ctk.CTkFrame(self, width=250)
        self.progress_frame.pack(pady=10)
        self.progress_frame.pack_propagate(False)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_columnconfigure(1, weight=3)
        # 250-70 = 180
        self.label_progress_bar = ctk.CTkLabel(self.progress_frame, width=70, text="Copying modules", font=("Helvetica", 10, "bold"), wraplength=70)
        self.model_progress_bar = ctk.CTkProgressBar(self.progress_frame, width=180)

        self.label_sphinx_progress_bar = ctk.CTkLabel(self.progress_frame, width=70,text="Creating sphinx", font=("Helvetica", 10, "bold"), wraplength=70)
        self.sphinx_progress_bar = ctk.CTkProgressBar(self.progress_frame, width=180)

        self.label_progress_bar_zip = ctk.CTkLabel(self.progress_frame,width=70, text="Creating zip", font=("Helvetica", 10, "bold"), wraplength=70)
        self.zip_progress_bar = ctk.CTkProgressBar(self.progress_frame, width=180)
        self.label_progress_bar.grid(row=0, column=0, padx=5, pady=5)
        self.model_progress_bar.set(0)
        self.model_progress_bar.grid(row=0, column=1, padx=5, pady=5)
        self.label_sphinx_progress_bar.grid(row=1, column=0, padx=5, pady=5)
        self.sphinx_progress_bar.set(0)
        self.sphinx_progress_bar.grid(row=1, column=1, padx=5, pady=5)
        self.label_progress_bar_zip.grid(row=2, column=0, padx=5, pady=5)
        self.zip_progress_bar.set(0)
        self.zip_progress_bar.grid(row=2, column=1, padx=5, pady=5)

    def create_sphinx_doc(self) -> None:
        """
        This method is used to create a new branch in all local repositories

        :param: None

        :returns: None
        """
        self.create_progress_bar()
        self.model_progress_bar.set(0.05)
        mip_version_name = self.mip_version.get()
        self.model_progress_bar.set(0.1)
        zip_file_password_name = self.zip_file_password.get()
        self.model_progress_bar.set(0.15)
        if not mip_version_name:
            self.root.show_alert("Please enter a name of a MIP version!")
            self.close_popup()
            return
        if not zip_file_password_name:
            self.root.show_alert("Please enter a name of a Zip file password!")
            self.close_popup()
            return
        if mip_version_name == zip_file_password_name:
            self.root.show_alert(
                "Please enter a different name for the MIP version "
                "and Zip file password!"
            )
            self.close_popup()
            return
        logger(f"Create processing create sphinx documentation with {mip_version_name}")

        repos_data, _ = get_json_data()
        self.model_progress_bar.set(0.2)

        if repos_data:
            self.add_button.configure(state="disabled")
            self.mip_version.configure(state="disabled")
            self.zip_file_password.configure(state="disabled")

            all_repositories = repos_data.keys()

            try:
                path_local_modules = os.path.join(script_path, "local_modules")
                if os.path.exists(path_local_modules):
                    shutil.rmtree(path_local_modules)
                os.mkdir(path_local_modules)

                preparing_files_and_folders_sphinx(
                    all_repositories, self.model_progress_bar
                )
                self.model_progress_bar.set(2)
                self.model_progress_bar.configure(progress_color="green")

                update_progress_bar_sphinx = thread_with_trace(
                    target=self.update_sphinx_progress_bar
                )
                update_progress_bar_sphinx.start()

                launch_sphinx_api(mip_version_name)
                update_progress_bar_sphinx.kill()
                self.sphinx_progress_bar.set(0.99)
                self.sphinx_progress_bar.configure(progress_color="green")
                self.sphinx_progress_bar.set(1.0)
                file_zip, folder_path = create_zip_file_sphinx_build(
                    zip_file_password_name, self.zip_progress_bar
                )
                self.zip_progress_bar.set(1)
                self.zip_progress_bar.configure(progress_color="green")
                logger(f"The zip file has been created successfully! {file_zip}")

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
                        "Opening folders is not supported on "
                        f"the {current_platform} platform."
                    )

            except Exception as e:
                logger("Failed to create the Zip file!", "error")
                logger(e, "critical")

            self.close_popup()
            self.root.show_alert("The zip file has been created successfully!")

    def update_sphinx_progress_bar(self):
        """
        This method is used to update the progress bar

        :param: None

        :returns: None
        """
        nb_files = count_files(os.path.join(script_path, "local_modules"), ".py") * 3
        docs_folder_path = os.path.join(script_path, "docs")
        rst_count = 0
        html_count = 0
        doctree_files = 0
        while (doctree_files + html_count + rst_count) < nb_files:
            # Count .rst files in docs/source
            rst_count = count_files(os.path.join(docs_folder_path, "source"), ".rst")

            # Count .html files in docs/build
            html_count = count_files(os.path.join(docs_folder_path, "build"), ".html")

            doctree_files = count_files(
                os.path.join(docs_folder_path, "build", "_doctrees"), ".doctree"
            )
            self.sphinx_progress_bar.set(
                (html_count + rst_count + doctree_files + 9) / nb_files
            )
        self.sphinx_progress_bar.set(2)
