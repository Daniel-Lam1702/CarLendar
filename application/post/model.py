import sys
sys.path.append(".")
from application.model_extension import db
from datetime import datetime
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default = datetime.utcnow())
    forum = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #replies = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True) #Children posts for the post
    
    def serialize(self):
        return {'post_id': self.id, 'title': self.title, 'content': self.content, 'forum': self.forum, 'date': self.date, 'user_id': self.user_id}
    