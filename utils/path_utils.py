import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def resource_path(relative_path: str) -> str:
    """Return absolute path to resource, compatible with PyInstaller."""
    base = getattr(sys, '_MEIPASS', BASE_DIR)
    return os.path.join(base, relative_path)
