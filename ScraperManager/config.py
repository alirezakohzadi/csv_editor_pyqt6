# config.py
from pathlib import Path

APP_NAME = "Scraper Manager"
VERSION = "1.0.0"

# پوشه‌ای که فایل‌های اسکرپر داخل آن قرار دارند
DATA_DIR = Path.cwd()

# فرمت‌های قابل پشتیبانی
SUPPORTED_EXTENSIONS = [
    ".csv",
    ".xlsx",
    ".json"
]

# کلمات کلیدی برای تشخیص نوع فایل
NEWS_KEYWORDS = [
    "news",
    "article",
    "post"
]

DRUG_KEYWORDS = [
    "drug",
    "medicine",
    "medicines",
    "pharma"
]

GROUP_KEYWORDS = [
    "group",
    "groups",
    "telegram",
    "channel"
]

BACKUP_FOLDER = "backups"

AUTO_BACKUP = True

AUTO_REFRESH = True

REFRESH_INTERVAL = 5000

DARK_MODE = False