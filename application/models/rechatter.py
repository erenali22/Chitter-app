from application import db
from datetime import datetime

now = datetime.now()

current_time = now

  

class ReChatter(db.Model):
    rechatter_id = db.Column(db.Integer, primary_key=True)
    rechatter_user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE' ), nullable=False)
    r_chatter_id =  db.Column(db.Integer, db.ForeignKey('chatter.chatter_id' ), nullable=False)
    rechatter_created_at = db.Column(db.DateTime, nullable=False, default=current_time)
    rechatter_updated_at = db.Column(db.DateTime, nullable=True,onupdate=current_time,default=current_time)
    original_chatter_id = db.Column(db.Integer,db.ForeignKey('chatter.chatter_id'))
   
