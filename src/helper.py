from pathlib import Path
import sys

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        # Project root when running from source
        base = Path(__file__).resolve().parent.parent

    return base / relative_path