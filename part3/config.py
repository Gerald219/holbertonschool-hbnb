class DevConfig:
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb_dev.db"
    JWT_SECRET_KEY = "dev-secret-key"  # will move to .env hidden 

class ProdConfig:
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/hbnb"
    JWT_SECRET_KEY = "change-me-in-prod"
