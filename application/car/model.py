import sys
sys.path.append(".")
from application.model_extension import db
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(18), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def add_miles(self, miles):
        self.mileage += miles
    
    def serialize(self):
        return {'car_id': self.id, 'vin': self.vin, 'make': self.make, 'model': self.model, 'year': self.year, 'color': self.color, 'mileage': self.mileage, 'user_id': self.user_id}