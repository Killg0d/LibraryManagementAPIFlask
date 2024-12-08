class Config:
    """Base config class with default settings."""
    SECRET_KEY = 'mysecretkey'

class TestingConfig(Config):
    """Test config class with SQLite in-memory database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
