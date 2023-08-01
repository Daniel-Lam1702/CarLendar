import sys
sys.path.append(".")
from application.user.model import User
from application.model_extension import db
def update_user_activity(user_id):
    ###Updating the time of the user activity
    user = db.session.get(User, int(user_id))
    user.updateLastActive()
    db.session.commit() #Commiting the changes