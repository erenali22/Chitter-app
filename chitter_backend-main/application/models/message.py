from application import db,ma
from datetime import datetime
now = datetime.now()

current_time = now

  
class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE' ), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE' ), nullable=False)
    message_content =db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=current_time, nullable=False)
