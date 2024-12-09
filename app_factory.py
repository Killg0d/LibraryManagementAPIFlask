from db.database import initialize_db, get_db_connection
from flask import Flask
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from models.user import create_user

def create_app(config_name="development"):
    """
    Application factory to create and configure a Flask application instance.

    Args:
        config_name (str, optional): The configuration to use for the application.
                                     Options are "development", "testing", and "production".
                                     Defaults to "development".

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Set the app's configuration based on the environment
    if config_name == "testing":
        app.config.from_object(TestingConfig)
    elif config_name == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)  # Defaults to development configuration

    # Initialize the database and optionally add a test user
    with app.app_context():
        initialize_db()
        add_test_user()

    return app

def add_test_user():
    """
    Add a default test user to the database for development or testing purposes.
    """
    create_user("testuser", "testpassword")
