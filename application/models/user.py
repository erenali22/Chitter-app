from application import db
from datetime import datetime
now = datetime.now()

current_time = now

  
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String)
    intrests = db.Column(db.String)

    bio = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=current_time)
    updated_at = db.Column(db.DateTime, nullable=True)

    
   

