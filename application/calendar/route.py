"""After Loging in the user, a token must be created and with the token the data from the user can be accessed"""
###

"""Creating a Calendar for each car created
    we can fetch the data from the table Maintainance Calendar which will provide us the required mileage to make a car fix
    We will have a post request because we need the token to access the mileage of the car of the user 
"""
"""
@app.route('/create_calendar', methods=['POST'])
def create_calendar():
    # Obtaining the token
    auth_token = request.headers.get('Authorization')
    print(auth_token)
    if not auth_token:
        return jsonify({'message': 'Missing authorization token'}), 401
    # decoding the token into the user id
    user_id = decode_auth_token(auth_token)
    if isinstance(user_id, str):
        return jsonify({'message': user_id}), 401

    generate_car_fix()

def generate_car_fix():
    """
### Initializes and runs the backend of the app