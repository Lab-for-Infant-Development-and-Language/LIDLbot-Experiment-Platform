from pathlib import Path
from tkinter import Tk, filedialog

from app.core.exceptions import NoDirectorySelected

def select_directory_dialog(prompt="Select Directory"):
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.update()
    try:
        directory = filedialog.askdirectory(title=prompt)
    finally:
        root.destroy()
    if not directory:
        raise NoDirectorySelected(f"No directory selected.")
    return Path(directory).resolve()