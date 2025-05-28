import sys
import os

def resource_path(relative_path):
    """Get the absolute path to resource, works for dev and PyInstaller"""
    try:
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    except Exception:
        return os.path.join(os.path.abspath("."), relative_path)