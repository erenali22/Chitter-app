from application import db
from datetime import datetime

now = datetime.now()

current_time = now

  

class Chatter(db.Model):
    chatter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE' ), nullable=False)
    chatter_content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=current_time)
    updated_at = db.Column(db.DateTime, nullable=True)
    media = db.Column(db.String, nullable=True)  
    media_type = db.Column(db.String, nullable=True)  
    original_chatter_id = db.Column(db.ForeignKey('chatter.chatter_id'),nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    chatter_publish_type = db.Column(db.String,default='published')
   
    category = db.Column(db.String,nullable=True)
   

    
