# database.py

import shutil
from pathlib import Path

import pandas as pd

from config import *

class Database:

    def __init__(self):
        self.files = {
            "news": [],
            "drugs": [],
            "groups": [],
            "other": []
        }

        self.scan()

    # --------------------------------

    def scan(self):

        self.files = {
            "news": [],
            "drugs": [],
            "groups": [],
            "other": []
        }

        for file in DATA_DIR.iterdir():

            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            name = file.stem.lower()

            if any(k in name for k in NEWS_KEYWORDS):
                self.files["news"].append(file)

            elif any(k in name for k in DRUG_KEYWORDS):
                self.files["drugs"].append(file)

            elif any(k in name for k in GROUP_KEYWORDS):
                self.files["groups"].append(file)

            else:
                self.files["other"].append(file)

        return self.files

    # --------------------------------

    def load(self, path):

        path = Path(path)

        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)

        elif path.suffix.lower() == ".xlsx":
            return pd.read_excel(path)

        elif path.suffix.lower() == ".json":
            return pd.read_json(path)

        raise Exception("Unsupported File")

    # --------------------------------

    def save(self, df, path):

        path = Path(path)

        self.backup(path)

        if path.suffix.lower() == ".csv":
            df.to_csv(path, index=False)

        elif path.suffix.lower() == ".xlsx":
            df.to_excel(path, index=False)

        elif path.suffix.lower() == ".json":
            df.to_json(path,
                       orient="records",
                       force_ascii=False,
                       indent=4)

    # --------------------------------

    def backup(self, path):

        if not AUTO_BACKUP:
            return

        backup_dir = DATA_DIR / BACKUP_FOLDER

        backup_dir.mkdir(exist_ok=True)

        dst = backup_dir / path.name

        shutil.copy(path, dst)

    # --------------------------------

    def delete_rows(self, df, rows):

        rows = sorted(rows, reverse=True)

        for row in rows:
            df.drop(row, inplace=True)

        df.reset_index(drop=True, inplace=True)

        return df

    # --------------------------------

    def search(self, df, text):

        if text == "":
            return df

        mask = df.astype(str).apply(
            lambda col:
            col.str.contains(text,
                             case=False,
                             na=False)
        )

        return df[mask.any(axis=1)]

    # --------------------------------

    def export_csv(self, df, filename):

        df.to_csv(filename, index=False)

    # --------------------------------

    def export_excel(self, df, filename):

        df.to_excel(filename, index=False)

    # --------------------------------

    def rename_file(self, old_path, new_name):

        old_path = Path(old_path)

        new_path = old_path.parent / new_name

        old_path.rename(new_path)

        return new_path

    # --------------------------------

    def delete_file(self, path):

        path = Path(path)

        if path.exists():
            path.unlink()

    # --------------------------------

    def info(self):

        return {
            "news": len(self.files["news"]),
            "drugs": len(self.files["drugs"]),
            "groups": len(self.files["groups"]),
            "other": len(self.files["other"])
        }

    # --------------------------------

    def all_files(self):

        files = []

        for key in self.files:

            files.extend(self.files[key])

        return files

    # --------------------------------

    def refresh(self):

        return self.scan()