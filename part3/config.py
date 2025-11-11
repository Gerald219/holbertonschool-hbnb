from datetime import timedelta
from pathlib import Path

# compute repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
DEV_DB_PATH = REPO_ROOT / "hbnb_dev.db"

class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEV_DB_PATH}"
    JWT_SECRET_KEY = "change-me-dev"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class ProdConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/hbnb"
    JWT_SECRET_KEY = "change-me-in-prod"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
