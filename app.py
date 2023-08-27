from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key' # Change this to secret key later
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/phantom_letter_db'
db = SQLAlchemy(app)

# TODO: Import and confogure user authentication

# TODO: Define database models

# TODO: Define API endpoints

if __name__ == '__main__':
    app.run(debug=True)