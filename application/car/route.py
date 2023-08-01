from flask import Blueprint
from application.car.model import Car
car = Blueprint(
    'car', __name__, static_folder='static', url_prefix='/car'
    )

#Getting the information of the cars of the user (GET)
#Getting the make of the cars of the user (GET)
#Creating a Car for the user (POST)
#Update the Mileage of the car
#Update the mileage of the car from two coordinates (One initial coordinate to final coordinate)