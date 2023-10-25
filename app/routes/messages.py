import flask
from flask import Blueprint, request, jsonify, abort
from app.models import User, Message, db
from app.utils.encryption import load_key_from_file, rsa_encrypt, rsa_decrypt

bp = Blueprint('messages', __name__, url_prefix='/messages')

@bp.route('/send', methods=['POST'])
def send_message():
  data = request.get_json()
  sender_username = data.get('sender_username')
  recipient_username = data.get('recipient_username')
  message = data.get('message')
  encrypted_symmetric_key = data.get('encrypted_symmetric_key')

  # Data validation
  if not sender_username or not recipient_username or not message or not encrypted_symmetric_key:
    return abort(400, description='Missing sender, recipient, message, or encrypted symmetric key')
  
  # Check if sender and recipient exist
  sender = User.query.filter_by(username=sender_username).first()
  recipient = User.query.filter_by(username=recipient_username).first()
  if not sender or not recipient:
    return abort(400, description='Incorrect sender or recipient')
  
  # Load the sender's private key
  sender_private_key = load_key_from_file(f'{sender_username}_private.pem', sender.password)

  # Decrypt the symmetric key
  symmetric_key = rsa_decrypt(sender_private_key, encrypted_symmetric_key)

  # Load the recipient's public key
  recipient_public_key = load_key_from_file(f'{recipient_username}_public.pem', None)

  # Encrypt the message
  encrypted_message = rsa_encrypt(recipient_public_key, message)

  # Create a new message
  message = Message(sender_id=sender.id, recipient_id=recipient.id, message=encrypted_message, symmetric_key=symmetric_key)
  db.session.add(message)
  db.session.commit()

  return jsonify(message='Message sent successfully')

@bp.route('/<username>', methods=['GET'])
def get_messages(username):
  # Check if user exists
  user = User.query.filter_by(username=username).first()
  if not user:
    return abort(400, description='Incorrect username')
  
  # Get all messages sent to the user
  messages = Message.query.filter_by(recipient_id=user.id).all()
  messages = [message.serialize() for message in messages]

  return jsonify(messages=messages)

@bp.route('/<username>/decrypt', methods=['POST'])
def decrypt_messages(username):
  data = request.get_json()
  encrypted_messages = data.get('encrypted_messages')

  # Data validation
  if not encrypted_messages:
    return abort(400, description='Missing encrypted messages')
  
  # Check if user exists
  user = User.query.filter_by(username=username).first()
  if not user:
    return abort(400, description='Incorrect username')
  
  # Load the user's private key
  user_private_key = load_key_from_file(f'{username}_private.pem', user.password)

  # Decrypt the messages
  decrypted_messages = []
  for message in encrypted_messages:
    decrypted_message = rsa_decrypt(user_private_key, message)
    decrypted_messages.append(decrypted_message)

  return jsonify(decrypted_messages=decrypted_messages)
