"""
Tjhis is the main entry point for the application.
"""
from app.interface import MultiRepoManager

if __name__ == "__main__":
    branch_editor = MultiRepoManager()
    branch_editor.run()
