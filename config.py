class Config:
    """Base config class with common settings."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DATABASE_URI = 'sqlite:///dev_database.db'  # Local SQLite database for development

class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True
    DATABASE_URI = 'sqlite:///test_database.db'  # Separate SQLite database for testing

class ProductionConfig(Config):
    """Configuration for production environment."""
    DATABASE_URI = 'sqlite:///prod_database.db'  # SQLite for production (can be a file or server-based)
