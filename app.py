from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key' # Change this to secret key later
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/phantom_letter_db'
db = SQLAlchemy(app)

# TODO: Import and confogure user authentication
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view function

# TODO: Define database models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# TODO: Define API endpoints

if __name__ == '__main__':
    app.run(debug=True)