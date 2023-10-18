import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
  # Flask app configuration
  SECRET_KEY = os.getenv('SECRET_KEY')
  DEBUG = True
  TESTING = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # Database configuration
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL')

class ProductionConfig(Config):
  DEBUG = False
  TESTING = False

config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig,
  'default': 'development'
}