import os
import json
import shutil
from datetime import datetime


def resource_path(relative_path):
    """
    Return absolute path for development and PyInstaller.
    """
    try:
        import sys
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def ensure_dir(path):
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def load_json(path, default=None):
    """Load JSON file safely."""
    if default is None:
        default = {}

    if not os.path.exists(path):
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    """Save JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def backup_file(path, backup_dir="backup"):
    """Create backup copy of a file."""
    if not os.path.exists(path):
        return None

    ensure_dir(backup_dir)

    filename = os.path.basename(path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_name = f"{timestamp}_{filename}"
    backup_path = os.path.join(backup_dir, backup_name)

    shutil.copy2(path, backup_path)

    return backup_path


def format_date(date_obj=None):
    """Return formatted datetime string."""
    if date_obj is None:
        date_obj = datetime.now()

    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def human_size(size):
    """Convert bytes to human readable."""
    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{value:.2f} PB"


def clear_table(table):
    """Clear QTableWidget."""
    table.setRowCount(0)


def set_table_headers(table, headers):
    """Set table headers."""
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)


def center_window(window):
    """Center window on screen."""
    screen = window.screen().availableGeometry()
    geometry = window.frameGeometry()
    geometry.moveCenter(screen.center())
    window.move(geometry.topLeft())


def open_file(path):
    """Open file with default application."""
    if not os.path.exists(path):
        return

    if os.name == "nt":
        os.startfile(path)
    else:
        import subprocess
        subprocess.call(["xdg-open", path])


def timestamp():
    """Current unix timestamp."""
    return int(datetime.now().timestamp())


def log(message):
    """Simple console logger."""
    print(f"[{format_date()}] {message}")