from application import db
from datetime import datetime
now = datetime.now()

current_time = now

  
class Reply(db.Model):

    reply_id = db.Column(db.Integer, primary_key=True)
    reply_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=current_time)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)

    chatter_id = db.Column(db.Integer, db.ForeignKey('chatter.chatter_id',ondelete='CASCADE' ), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE' ), nullable=False)

    

