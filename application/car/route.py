import json, requests
from flask import Blueprint, jsonify, request
from application.car.model import Car
import sys

sys.path.append(".")
from application.user.model import User
from application.auth.auth import decode_auth_token, update_token
from application.model_extension import db
from application.route_extension import update_user_activity
car = Blueprint(
    'car', __name__, static_folder='static', url_prefix='/car'
    )
def got_results(object):
    return object != None
#Creating a Car for the user (POST)
@car.route("/create", methods = ['POST'])
def create():
    ### We just need a vin, color, mileage, and the token
    ###Authenticating the user###
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    user_id = decode_auth_token(auth_token)
    ###Authenticating the VIN###
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 401
    vin = str(request.json.get('vin'))
    ###Making an http request to an external database to get the information from the vin
    response_API = requests.get("https://auto.dev/api/vin/"+vin+"?apikey=ZrQEPSkKbGFtZGFuaWVsMTcwMkBnbWFpbC5jb20=")
    data = response_API.text
    parse_json = json.loads(data)
    if "message" in parse_json:
        return jsonify({'auth_token': auth_token, 'message': parse_json["message"]}), 400
    ###Else the vin is valid. Proceed to create the car
    car = Car(vin = vin, make = parse_json["make"]["name"], model = parse_json["model"]["name"], year = parse_json["years"][0]["year"], color = request.json.get('color'), mileage = request.json.get('mileage'),user_id = user_id)
    db.session.add(car)
    db.session.commit()
    ### updating the user activity
    update_user_activity(user_id)
    ### updating the token
    auth_token = update_token(auth_token)
    return jsonify({'auth_token':str(auth_token), 'car': car.id}) ##Car was created and its id is returned.
#Getting the information of the car id's of the user (GET)
@car.route("/get-cars", methods = ['GET'])
def get_cars():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    user_id = decode_auth_token(auth_token)
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 401
    #Getting all the cars owned by the user
    cars = Car.query.filter_by(user_id = user_id).all()
    #Getting the id of each car
    cars_id = [automobile.id for automobile in cars]
    ### updating the user activity
    update_user_activity(user_id)
    ### updating the token
    auth_token = update_token(auth_token)
    return jsonify({'auth_token':str(auth_token), 'cars_id':cars_id})
#Getting the make of the car from its id(GET)
@car.route("/get-make", methods = ['GET'])
def get_make():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    user_id = decode_auth_token(auth_token)
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 404
    car_id = request.json.get('car_id')
    car = Car.query.filter_by(id = car_id).first()
    if(got_results(car)):
        make = car.make
        ###Updating the time of the user activity
        update_user_activity(user_id)
        auth_token = update_token(auth_token)
        return jsonify({'auth_token':str(auth_token), 'make':make}), 201
    else:
        return jsonify({'auth_token':str(auth_token), 'message': "Car not found"}), 404 

#Get the mileage of the car from its id (GET)
@car.route("/get-mileage", methods = ['GET'])
def get_mileage():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    user_id = decode_auth_token(auth_token)
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 401
    car_id = request.json.get('car_id')
    car = Car.query.filter_by(id = car_id).first()
    mileage = car.mileage
    if(got_results(car)):
         ###Updating the time of the user activity
        update_user_activity(user_id)
        auth_token = update_token(auth_token)
        return jsonify({'auth_token':str(auth_token), 'mileage':mileage})
    else:
        return jsonify({'auth_token':str(auth_token), 'message': "Car not found"}), 404 
#Get the information of the car from its id
@car.route("/get-information", methods = ['GET'])
def get_car_information():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    user_id = decode_auth_token(auth_token)
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 401
    car_id = request.json.get('car_id')
    car = Car.query.filter_by(id = car_id).first()
    if(got_results(car)):
         ###Updating the time of the user activity
        update_user_activity(user_id)
        auth_token = update_token(auth_token)
        return jsonify({'auth_token':str(auth_token), 'car': car.serialize()}), 201
    else:
        return jsonify({'auth_token':str(auth_token), 'message': "Car not found"}), 404 
#Update the Mileage of the car (UPDATE)
#Update the mileage of the car from two coordinates (One initial coordinate to final coordinate)


