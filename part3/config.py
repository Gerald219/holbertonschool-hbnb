from datetime import timedelta


class DevConfig:
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb_dev.db"
    JWT_SECRET_KEY = "change-me-dev"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class ProdConfig:
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/hbnb"
    JWT_SECRET_KEY = "change-me-in-prod"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    