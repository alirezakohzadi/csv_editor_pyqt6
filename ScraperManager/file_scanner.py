# file_scanner.py

from pathlib import Path

import pandas as pd

from config import *


class FileScanner:

    def __init__(self, root=None):

        self.root = Path(root or DATA_DIR)

        self.files = {
            "news": [],
            "drugs": [],
            "groups": [],
            "other": []
        }

    # -----------------------------------------

    def scan(self):

        self.files = {
            "news": [],
            "drugs": [],
            "groups": [],
            "other": []
        }

        for file in self.root.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            category = self.detect(file)

            self.files[category].append(file)

        return self.files

    # -----------------------------------------

    def detect(self, file):

        name = file.stem.lower()

        if any(x in name for x in NEWS_KEYWORDS):
            return "news"

        if any(x in name for x in DRUG_KEYWORDS):
            return "drugs"

        if any(x in name for x in GROUP_KEYWORDS):
            return "groups"

        try:

            df = self.load(file, rows=3)

            cols = [
                str(c).lower()
                for c in df.columns
            ]

            text = " ".join(cols)

            if any(k in text for k in NEWS_KEYWORDS):
                return "news"

            if any(k in text for k in DRUG_KEYWORDS):
                return "drugs"

            if any(k in text for k in GROUP_KEYWORDS):
                return "groups"

        except Exception:
            pass

        return "other"

    # -----------------------------------------

    def load(self, path, rows=None):

        path = Path(path)

        ext = path.suffix.lower()

        if ext == ".csv":
            return pd.read_csv(path, nrows=rows)

        if ext == ".xlsx":
            return pd.read_excel(path, nrows=rows)

        if ext == ".json":
            return pd.read_json(path)

        raise Exception("Unsupported file")

    # -----------------------------------------

    def all_files(self):

        result = []

        for category in self.files:

            for file in self.files[category]:

                result.append(file)

        return result

    # -----------------------------------------

    def stats(self):

        return {
            "news": len(self.files["news"]),
            "drugs": len(self.files["drugs"]),
            "groups": len(self.files["groups"]),
            "other": len(self.files["other"]),
            "total": len(self.all_files())
        }

    # -----------------------------------------

    def reload(self):

        return self.scan()

    # -----------------------------------------

    def add_folder(self, folder):

        folder = Path(folder)

        if folder.exists():
            self.root = folder

    # -----------------------------------------

    def exists(self, file):

        return Path(file).exists()

    # -----------------------------------------

    def remove(self, file):

        file = Path(file)

        if file.exists():
            file.unlink()

    # -----------------------------------------

    def rename(self, file, new_name):

        file = Path(file)

        new_path = file.parent / new_name

        file.rename(new_path)

        return new_path

    # -----------------------------------------

    def backup(self, file):

        file = Path(file)

        backup_dir = self.root / BACKUP_FOLDER

        backup_dir.mkdir(exist_ok=True)

        target = backup_dir / file.name

        target.write_bytes(file.read_bytes())

        return target

    # -----------------------------------------

    def find(self, keyword):

        keyword = keyword.lower()

        result = []

        for file in self.all_files():

            if keyword in file.name.lower():
                result.append(file)

        return result