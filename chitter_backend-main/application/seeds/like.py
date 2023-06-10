from flask import request,jsonify
from application.models.like import Like
from application.schemas.like_schema import LikeSchema
from application import db


def like_chatter():
    user_id = request.form.get('user_id')
    chatter_id = request.form.get('chatter_id')
    like = Like(user_id=user_id, chatter_id=chatter_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({
        "is_liked":True,
        "status":"chatter has been liked"
    })

def unlike_chatter():
    user_id = request.form.get('user_id')
    chatter_id = request.form.get('chatter_id')
    unlike = Like.query.filter_by(user_id=user_id,chatter_id=chatter_id).first()
    db.session.delete(unlike)
    db.session.commit()
    return jsonify({
        "is_unliked":True,
        "status":"chatter has been unliked"
    })