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