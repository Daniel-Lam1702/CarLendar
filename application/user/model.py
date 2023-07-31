from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import sys

sys.path.append(".")
from application.model_extension import db
from application.car.model import Car
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    owned_cars = db.relationship('Car', backref='owner', lazy=True)
    last_active = db.Column(db.DateTime, default = datetime.utcnow())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def verify_password(self,input_password):
        return check_password_hash(self.password, input_password)
    
    def updateLastActive(self):
        self.last_active = datetime.utcnow()

    def get_last_active(self):
        return self.last_active

sys.path.remove(".")