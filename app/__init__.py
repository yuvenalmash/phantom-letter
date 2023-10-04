from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# Create a SQLAlchemy database instance
db = SQLAlchemy()

def create_app(config_name):
  # Create a Flask app instance
  app = Flask(__name__)

  # Set the app config values
  app.config.from_object(config[config_name])

  # Initialize the database
  db.init_app(app)

  # Import and register the blueprints (routes)
  from app.routes import auth, messages
  app.register_blueprint(auth.bp)
  app.register_blueprint(messages.bp)

  return app