from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user
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
# Example sending message route
@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    recipient_username = request.json.get('recipient')
    content = request.json.get('content')
    
    recipient = User.query.filter_by(username=recipient_username).first()
    if recipient:
        message = Message(sender_id=current_user.id, recipient_id=recipient.id, content=content)
        db.session.add(message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'}), 200
    else:
        return jsonify({'error': 'Recipient not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)