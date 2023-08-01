from flask import Flask
import sys
sys.path.append(".")
from application.model_extension import db

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3307/Carlendar"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Initialize Flask extensions here    
    import sys
    sys.path.append(".")

    # Register blueprints here
    from application.user.route import user as user_bp
    app.register_blueprint(user_bp)

    from application.post.route import post as post_bp
    app.register_blueprint(post_bp)

    from application.car.route import car as car_bp
    app.register_blueprint(car_bp)
    
    db.init_app(app)
    with app.app_context():    
        try:
          db.create_all()
        except Exception as exception:
          print("got the following exception when attempting db.create_all() in __init__.py: " + str(exception))
        finally:
          print("db.create_all() in __init__.py was successfull - no exceptions were raised")



    return app