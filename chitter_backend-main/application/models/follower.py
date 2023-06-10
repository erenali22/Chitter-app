from application import db
from datetime import datetime
now = datetime.now()

current_time = now

  
class Follower(db.Model):
    follower_p_id = db.Column(db.Integer,primary_key=True)
    followed_user = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE' ))
    followed_by = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE' ))
   
    timestamp = db.Column(db.DateTime, default=current_time)
