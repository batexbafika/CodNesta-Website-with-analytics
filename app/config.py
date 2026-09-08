import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Absolute path to the project root: C:\Users\batex\Desktop\CODNESTA
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to instance directory
INSTANCE_DIR = BASE_DIR / "instance"

# Ensure the instance directory physically exists on disk
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

# Build a clean cross-platform SQLite URI (using 3 slashes with as_posix())
DEFAULT_DB_URI = f"sqlite:///{(INSTANCE_DIR / 'codnesta.db').as_posix()}"


class Config:
    """Base configuration with shared defaults."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Uses DATABASE_URL if set in .env, otherwise defaults to the dynamically built path
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DEFAULT_DB_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in [
        "true",
        "on",
        "1",
    ]
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() in [
        "true",
        "on",
        "1",
    ]
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")

    MAIL_DEFAULT_SENDER = (
        "CodNesta Team",
        os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME")),
    )
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "contact@codnesta.com")

    # Flask-Limiter Default Settings
    RATELIMIT_DEFAULT = "200 per day; 50 per hour"
    RATELIMIT_STORAGE_URI = "memory://"


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration."""

    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}