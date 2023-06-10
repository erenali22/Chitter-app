from application import db
from datetime import datetime
now = datetime.now()

current_time = now

  
class Like(db.Model):
    like_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE' ))
    chatter_id = db.Column(db.Integer, db.ForeignKey('chatter.chatter_id',ondelete='CASCADE' ))
    timestamp = db.Column(db.DateTime, default=current_time)
