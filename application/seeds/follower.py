from flask import  request,jsonify
from application import db
from flask import request
from application.models.follower import Follower
from application.schemas.follower_schema import FollowerSchema
from sqlalchemy import text


def follow_user():
    my_id = request.form.get('my_id')
    user_id = request.form.get('user_id')
    new_follow = Follower(followed_user=user_id,followed_by=my_id)
    db.session.add(new_follow)
    db.session.commit()
    
    return jsonify({
        "is_followed":True,
        "status":"successfully followed",
    })

def unfollow_user():
    my_id = request.args.get('my_id')
    user_id = request.args.get('user_id')
    followed_user = Follower.query.filter_by(followed_by=my_id,followed_user=user_id).first()
    db.session.delete(followed_user)
    db.session.commit()
    
    return jsonify({
        "is_deleted":True,
        "status":"deleted successfully",
    })

def get_followed_users():
    my_id = request.args.get('my_id')
    followed_users_sql = text("select *,(SELECT count(*) from follower where follower.followed_user=user.id AND follower.followed_by="+str(my_id)+") as is_followed  from follower LEFT JOIN user on user.id=follower.followed_user where followed_by="+str(my_id))
    engine = db.engine.execute(followed_users_sql)
    schema = FollowerSchema(many=True)
    followed_users = schema.dump(engine)
    return jsonify({
        "data":followed_users
    })

def get_my_followers():
    my_id = request.args.get('my_id')
    query = text("select *,(SELECT count(*) from follower where follower.followed_user=user.id AND follower.followed_by="+str(my_id)+") as is_followed  from follower LEFT JOIN user on user.id=follower.followed_by where followed_user="+str(my_id))
    engine = db.engine.execute(query)
    schema = FollowerSchema(many=True)
    followers = schema.dump(engine)

    return jsonify({
        "data":followers
    })

def get_another_user_followers():
    user_id = request.args.get('user_id')
    my_id = request.args.get('my_id')
    query = None

    if my_id:
        query = text("SELECT *,(SELECT count(*) from follower where follower.followed_user=user.id AND follower.followed_by="+str(my_id)+") as is_followed  FROM follower LEFT JOIN user on user.id=follower.followed_by WHERE followed_user="+str(user_id))
    else:
        query = text("SELECT * FROM follower  LEFT JOIN user on user.id=follower.followed_by WHERE followed_user="+str(user_id))
    engine = db.engine.execute(query)
    schema = FollowerSchema(many=True)
    followers = schema.dump(engine)
    return jsonify(({
        "data":followers
    }))


def get_another_user_followings():
    user_id = request.args.get('user_id')
    my_id = request.args.get('my_id')
    query = None

    if my_id:
        query = text("SELECT *,(SELECT count(*) from follower where follower.followed_user=user.id AND follower.followed_by="+str(my_id)+") as is_followed  FROM follower LEFT JOIN user on user.id=follower.followed_user WHERE followed_by="+str(user_id))
    else:
        query = text("SELECT * FROM follower  LEFT JOIN user on user.id=follower.followed_user WHERE followed_by="+str(user_id))
    engine = db.engine.execute(query)
    schema = FollowerSchema(many=True)
    followers = schema.dump(engine)
    return jsonify(({
        "data":followers
    }))