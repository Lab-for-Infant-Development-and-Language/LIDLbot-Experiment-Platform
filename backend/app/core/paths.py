import sys
from pathlib import Path


def _get_root_path():
    if hasattr(sys, '_MEIPASS') and getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).resolve().parent.parent.parent.parent

ROOT_PATH: Path = _get_root_path()
TEMPLATES_PATH = ROOT_PATH / "frontend" / "templates"
STATIC_PATH = ROOT_PATH / "frontend" / "static"