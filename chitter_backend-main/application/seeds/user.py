from flask import Blueprint,request,jsonify
from application.models.user import User
from application.schemas.user_schema import UserSchema
from application.schemas.chatter_schema import ChatterSchema
from application.schemas.follower_schema import FollowerSchema
from werkzeug.security import generate_password_hash,check_password_hash
from application import db
from application.seeds.utils import save_file,remove_file
from sqlalchemy import text
from application.schemas.rechatter_schema import ReChatterSchema

import geocoder
geo = geocoder.ip('me')
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    profile_picture = request.files.get('profile_picture')
    bio = request.form.get('bio')

    intrests = request.form.get('intrests')
    print(intrests)
    hashed_password = generate_password_hash(password)

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            "status":"Email Already Exist",
            "is_registered": False
        })

    else:
        is_saved,file_name = save_file(profile_picture, 'uploads')
        if is_saved == False:
            print("Could not save profile picture")
            return jsonify({
            "status":"Could not save profile picture",
            "is_registered": False
            })
        new_user = User(username=username,email=email,password=hashed_password,
        bio=bio,location=geo[0].__str__(),profile_picture=file_name,intrests=intrests)
        db.session.add(new_user)
        db.session.commit()

        user_schema = UserSchema(many=False)
    return jsonify({
            "status":"User Registered Successfully",
            "user":user_schema.dump(new_user),
            "is_registered": True
        })

def login_user():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email)
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password,password):
        users_schema = UserSchema(many=False)
        user = users_schema.dump(user)
        
       
        return jsonify({
            "user":user,
            "is_loggedin":True,
            "status":"Logged in successfully"
        })
    else:
        return jsonify({
           "is_loggedin":False,
            "status":"Invalid Email or Password"
        })


def get_users():
    my_id = request.args.get('my_id')
    users_query = None
    if my_id:
        users_query = text("SELECT *,(SELECT count(*) from follower where follower.followed_user=user.id AND follower.followed_by="+str(my_id)+") as is_followed FROM user WHERE id != "+str(my_id)+"")
    else:
        users_query = text("SELECT * FROM user")
    engine = db.engine.execute(users_query)
    schema = UserSchema(many=True)
    users_list = schema.dump(engine)

    return jsonify({
        "data":users_list
    })



def get_user():
    user_id = request.args.get('user_id')
    my_id = request.args.get('my_id')
    query = None
    chatters_query = None
    who_to_follow_query = None

    if my_id:
        query = text("SELECT *,(SELECT count(*) from follower where follower.followed_user=user.id AND follower.followed_by="+str(my_id)+") as is_followed,(SELECT count(*) from follower where follower.followed_user="+str(user_id)+") as number_of_followers,(SELECT count(*) FROM follower where follower.followed_by="+str(user_id)+") as number_of_following,(SELECT count(*) FROM chatter where chatter.user_id="+str(user_id)+") as number_of_chatters FROM user  WHERE id="+str(user_id)+"")
        chatters_query = text("SELECT *,(SELECT count(*) FROM like WHERE like.chatter_id=chatter.chatter_id) as likes_count,(SELECT count(*) FROM like where like.user_id="+str(my_id)+" and like.chatter_id=chatter.chatter_id) as is_liked,(SELECT count(*) FROM reply WHERE reply.chatter_id=chatter.chatter_id) as number_of_replies,(SELECT count(*) FROM chatter where chatter.user_id="+str(user_id)+") as number_of_chatters FROM chatter LEFT JOIN user on user.id=chatter.user_id  WHERE chatter.user_id="+str(user_id))
        who_to_follow_query = text("SELECT *,(SELECT count(*) FROM follower where follower.followed_user=user.id AND follower.followed_by="+str(my_id)+" ) as is_followed FROM follower LEFT JOIN user on user.id=follower.followed_user WHERE follower.followed_by="+str(user_id))

    else:
        query = text("SELECT *,(SELECT count(*) from follower where follower.followed_user="+str(user_id)+") as number_of_followers,(SELECT count(*) FROM follower where follower.followed_by="+str(user_id)+") as number_of_following FROM user WHERE id="+str(user_id)+"")
        chatters_query = text("SELECT *,(SELECT count(*) FROM like WHERE like.chatter_id=chatter.chatter_id) as likes_count,(SELECT count(*) FROM reply WHERE reply.chatter_id=chatter.chatter_id) as number_of_replies,(SELECT count(*) FROM chatter where chatter.user_id="+str(user_id)+") as number_of_chatters FROM chatter LEFT JOIN user on user.id=chatter.user_id  WHERE chatter.user_id="+str(user_id))
        who_to_follow_query = text("SELECT * FROM follower LEFT JOIN user on user.id=follower.followed_user WHERE follower.followed_by="+str(user_id))
        
    engine = db.engine.execute(query)
    schema = UserSchema(many=True)
    user = schema.dump(engine)


    chatters_engine = db.engine.execute(chatters_query)
    chatter_schema = ChatterSchema(many=True)
    chatters = chatter_schema.dump(chatters_engine)


    who_to_follow_engine = db.engine.execute(who_to_follow_query)
    schema= FollowerSchema(many=True)
    who_to_follow = schema.dump(who_to_follow_engine)

    rechatters= None
    rechatters_data = []
    for chatter in chatters:
        rechatters_query = text("SELECT * FROM re_chatter LEFT JOIN chatter on chatter.chatter_id=re_chatter.original_chatter_id LEFT JOIN user on user.id=chatter.user_id WHERE re_chatter.r_chatter_id="+str(chatter['chatter_id'])+"")

        engine = db.engine.execute(rechatters_query)
        rechatter_schema = ReChatterSchema(many=True)
        rechatters = rechatter_schema.dump(engine)
        rechatters_data.append(rechatters)


    return jsonify(({
        "data":user[0],
        "chatters":chatters,
        "who_to_follow":who_to_follow,
        "rechatter_data":rechatters_data
    }))



def update_user():
    user_id = request.form.get('user_id')
    
    email  = request.form.get('email')
    place = request.form.get('place')
    username = request.form.get('username')
    bio = request.form.get('bio')
    profile_image = request.files.get('profile_image')
    user = User.query.get(user_id)
 
    if email:
        check_email = User.query.filter_by(email=email).first()
        if check_email:
            return jsonify({
                "is_updated":False,
                "status":"Email Already Exists",
            })

        user.email = email
    
    if username:
        print(username)
        user.username = username
    
    if bio:
        user.bio = bio

    if place:
        user.location = place

    if profile_image:
        is_removed = remove_file(user.profile_picture, 'uploads')
        if is_removed == False:
            pass
        is_saved,file_name = save_file(profile_image, 'uploads')
        if is_saved == False:
            return jsonify({
            "is_updated":False,
            "status":"Could not save profile picture"
            })
        user.profile_picture = file_name
    
    db.session.commit()

    return jsonify({
        "is_updated":True,
        "status":"Profile Update Successfully"
    })



def change_password():
    user_id = request.form.get('user_id')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    user = User.query.get(user_id)
    check = check_password_hash(user.password, old_password)

    if check:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({
             "is_updated":True,
            "status":"Password Updated Successfully",
        })
    else:
        return jsonify({
            "is_updated":False,
            "status":"Old password did not match.Please try again"
        })


