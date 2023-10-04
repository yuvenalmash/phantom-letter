from datetime import datetime
from app import db

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(25), nullable=False, unique=True)
  password = db.Column(db.String(128), nullable=False)

  def __init__(self, username, password):
    self.username = username
    self.password = password

  def __repr__(self):
    return f'<User {self.username}>'
  
class Message(db.Model):
  __tablename__ = 'messages'

  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(512), nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  sender = db.relationship('User', foreign_keys=sender_id, backref='sent_messages')
  recipient = db.relationship('User', foreign_keys=recipient_id, backref='received_messages')

  def __init__(self, content, sender_id, recipient_id):
    self.content = content
    self.sender_id = sender_id
    self.recipient_id = recipient_id

  def __repr__(self):
    return f'<Message {self.id}>'
