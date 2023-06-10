from application import db

from datetime import datetime

now = datetime.now()


class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id',ondelete='CASCADE' ),nullable=False)
    created_for = db.Column(db.ForeignKey('user.id',ondelete='CASCADE' ),nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=now)
