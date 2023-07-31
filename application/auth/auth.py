import jwt
from datetime import datetime, timedelta, timezone
from flask import jsonify
import sys
sys.path.append(".")
from application.user.model import User
sys.path.append(".")
from main.app import db
"""
Creating the user token, verifying its validity, and decoding it
"""
### This function is encoding the user id into a token and returning it to the function that calls it
def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=15),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token
    except Exception as e:
        return e
### This Function verifies if the token passed the threshold time of being close to be expired
def verify_token_threshold(token):
    try:
        payload = jwt.decode(token.encode('utf-8'), 'secret', algorithms=['HS256'])  # Decodes the token without verification
        exp = payload.get('exp')  # Extracts the 'exp' claim from the payload
        print(exp)
        if exp:
            expiration = datetime.fromtimestamp(exp, timezone.utc)
            time_difference = expiration - datetime.now(timezone.utc)
            threshold = timedelta(minutes=5)
            return time_difference > threshold
    except jwt.InvalidTokenError:
        return False
    return False
### Returns a new token that will keep the user signed if they were active on the application less than 10 minutes before the expiration time
def update_token(token):
    try:
        update = verify_token_threshold(token)
        if update:
            print(12)
            return token
        else:
            print(24)
            user_id = decode_auth_token(token)  # Getting the user.id
            user = db.session.get(User, int(user_id))
            last_activity_time = user.get_last_active()  # Get the last activity time from the user's session
            payload = jwt.decode(token.encode('utf-8'), 'secret', algorithms=['HS256'])  # Decodes the token without verification
            exp = payload.get('exp')  # gets the expiration
            expiration = datetime.fromtimestamp(exp)  # converts the expiration into datetime
            time_difference = expiration - last_activity_time
            threshold = timedelta(minutes=10)  # Checks if the last time the user did an action in 10 minutes or less
            if time_difference <= threshold:  # if the action happened within 10 minutes. Then, create a new token
                return encode_auth_token(user_id)
            else:
                return jsonify({'message': 'Inactive token. Please log in again'}), 404
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token. Please log in again.'}), 401
### Decodes the token into the user id
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer: user.id
    """
    try:
        payload = jwt.decode(auth_token.encode('utf-8'), 'secret', algorithms=['HS256'])
        print(payload['sub'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'