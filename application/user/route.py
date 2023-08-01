from flask import Blueprint
from flask import request, jsonify,abort
from application.user.model import User
from http import HTTPStatus
import sys
sys.path.append("..")
from application.model_extension import db
from werkzeug.security import generate_password_hash
from application.auth.auth import decode_auth_token, encode_auth_token
user=Blueprint(
    'user', __name__, static_folder='static', url_prefix='/user'
    )
###Signing up the User###
@user.route('/signup', methods=['POST'])
def signup():
    print("hello")
    if request.method == 'POST':
        username = request.get_json().get('username')
        password = request.get_json().get('password')

        if (User.query.filter_by(username=username).first()):
            abort(409, 'User already exists')
    
        hashed_password = generate_password_hash(password)
        new_user = User(username, hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Success'}), HTTPStatus.OK
    return jsonify({'message': 'Method Not Allowed'}), 405

###Login the User###
@user.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Verify the username and password against the database
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        # Username and password are valid
        user_id = user.id

        # Generate authentication token
        try:
            auth_token = encode_auth_token(user_id)
            user.updateLastActive()
            db.session.commit()
            print(auth_token)
            return jsonify({'auth_token': str(auth_token)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        # Invalid username or password
        return jsonify({'message': 'Invalid credentials'}), 401


###Deleting a user###
@user.route('/delete', methods = ['DELETE'])
def delete_post():
    auth_token = request.headers.get('Authorization') #Retrieving the token of the user
    print(auth_token)
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    user_id = decode_auth_token(auth_token) #The user id is obtained after decoding the token
    username = request.json.get('username') #The username is going to be verified before deleting the user
    password = request.json.get('password') #The password is also verified before deleting the user.
