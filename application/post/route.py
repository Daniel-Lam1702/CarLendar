from flask import Blueprint
from flask import Blueprint
from flask import request, jsonify
import jwt
import sys
sys.path.append(".")
from application.user.model import User
from application.post.model import Post
from application.car.model import Car
from application.model_extension import db
from application.auth.auth import decode_auth_token, update_token
from application.route_extension import update_user_activity

post=Blueprint(
    'post', __name__, static_folder='static', url_prefix='/post'
    )

###Creating a post###
@post.route('/create', methods=['POST'])
def create_post():
    auth_token = request.headers.get('Authorization')
    print(auth_token)
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401

    user_id = decode_auth_token(auth_token)
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 401

    user = db.session.get(User, int(user_id))
    if not user:
        return jsonify({'message': 'User not found'}), 404

    title = request.json.get('title')
    content = request.json.get('content')
    forum = request.json.get('forum')
    new_post = Post(title=title, content=content, forum = forum, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()
    #updating the time and date
    update_user_activity(user_id)
    #updating the token
    auth_token = update_token(auth_token)
    #Verifying if the function returned a token
    try:
        jwt.decode(auth_token, verify=False)
        return jsonify({'auth_token': str(auth_token), 'message': 'Post created successfully'}), 201
    except jwt.InvalidTokenError:
        return auth_token
### Getting a list of posts depending on the criteria ###
@post.route('/get-posts-from-make', methods =['GET'])
def get_posts_for_make():
    #Retrieving token from the json to see if the user is still in session
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    #decoding the token into the user id
    user_id = decode_auth_token(auth_token)
    #Verifying if a user_id was returned. Otherwise an error happened.
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 401
    #Retrieving the car from the user
    make = request.json.get('make')
    posts = Post.query.filter_by(forum = make).all()
    #updating the time of the user last activity
    update_user_activity(user_id)
    auth_token = update_token(auth_token)
    return jsonify({'auth_token': str(auth_token),'posts':[post.serialize() for post in posts]})

### Getting a list of posts depending from the user id###
@post.route('/get-posts-from-user', methods =['GET'])
def get_posts_for_user():
    # retrieving the token in session
    auth_token = request.headers.get('Authorization')
    # checking if the token exists
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    #decoding the token into the user id
    user_id = decode_auth_token(auth_token)
    #Verifying if a user_id was returned. Otherwise an error happened.
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 401
    #Getting a list of posts made by the user
    posts = Post.query.filter_by(user_id=user_id).all()
    #updating the time of the user last activity
    update_user_activity(user_id)
    auth_token = update_token(auth_token)
    return jsonify({'auth_token': str(auth_token), 'posts':[post.serialize() for post in posts]})

###Deleting a post###
@post.route('/delete', methods = ['DELETE'])
def delete_post():
    auth_token = request.headers.get('Authorization') #Retrieving the token of the user
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    post_id = request.json.get('post_id')
    try:
        post = Post.query.filter_by(id=post_id).first()
        post_user_id = post.user_id
        session_user_id = decode_auth_token(auth_token)
    except:
        #In case the post is going to be deleted again and the post was already deleted, then the post cannot be deleted
        return jsonify({'auth_token': str(auth_token), 'message': 'Post was already deleted'}), 404
    if isinstance(session_user_id, str):
        return jsonify({'message': session_user_id}), 401
    if(session_user_id == post_user_id): #The user id is obtained after decoding the token. Verify if the owner is the one deleting the post
        db.session.delete(post)
        db.session.commit()
        ###Updating the time of the user activity
        update_user_activity(session_user_id)
        auth_token = update_token(auth_token)
        return jsonify({'auth_token': str(auth_token), 'message': 'Post deleted successfully'}), 201
    else:
        return jsonify({'message': 'No authorization to delete the post'}), 401
    



