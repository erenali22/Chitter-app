from flask import Blueprint,jsonify,request
from application import db
from application.models.chatter import Chatter
from application.models.rechatter import ReChatter
from application.models.user import User
from sqlalchemy import text
from application.models.location import Location
from application.seeds.utils import save_file,remove_file
import geocoder
geo = geocoder.ip('me')

from application.schemas.chatter_schema import ChatterSchema
from application.schemas.rechatter_schema import ReChatterSchema


def get_Chatters():
    user_interests = request.args.get('user_interests')
    
    chatters_query=None
    if user_interests:
        user_id = request.args.get('user_id')
        if user_id:
            chatters_query = text("SELECT *,(SELECT count(*) FROM like WHERE like.chatter_id=chatter.chatter_id) as likes_count,(SELECT count(*) FROM like where like.user_id="+str(user_id)+" and like.chatter_id=chatter.chatter_id) as is_liked,(SELECT count(*) FROM reply WHERE reply.chatter_id=chatter.chatter_id) as number_of_replies FROM chatters  LEFT JOIN users on users.id=chatter.user_id WHERE category IN "+user_interests)
        else:
            chatters_query = text("SELECT *,(SELECT count(*) FROM like WHERE like.chatter_id=chatter.chatter_id) as likes_count,(SELECT count(*) FROM reply WHERE reply.chatter_id=chatter.chatter_id) as number_of_replies FROM chatters  LEFT JOIN users on users.id=chatter.user_id WHERE category IN "+user_interests)

    else:
        user_id = request.args.get('user_id')
       
        if user_id:
            chatters_query =text("SELECT *,(SELECT count(*) FROM like WHERE like.chatter_id=chatter.chatter_id) as likes_count,(SELECT count(*) FROM like where like.user_id="+str(user_id)+" and like.chatter_id=chatter.chatter_id) as is_liked,(SELECT count(*) FROM reply WHERE reply.chatter_id=chatter.chatter_id) as number_of_replies FROM chatter LEFT JOIN user on user.id=chatter.user_id ")
        else:
            chatters_query =text("SELECT *,(SELECT count(*) FROM like WHERE like.chatter_id=chatter.chatter_id) as likes_count,(SELECT count(*) FROM reply WHERE reply.chatter_id=chatter.chatter_id) as number_of_replies FROM chatter LEFT JOIN user on user.id=chatter.user_id")

    engine = db.engine.execute(chatters_query)

    chatter_schema = ChatterSchema(many=True)
    chatters = chatter_schema.dump(engine)
    rechatters= None
    rechatters_data = []
    for chatter in chatters:
        rechatters_query = text("SELECT * FROM re_chatter LEFT JOIN chatter on chatter.chatter_id=re_chatter.original_chatter_id LEFT JOIN user on user.id=chatter.user_id WHERE re_chatter.r_chatter_id="+str(chatter['chatter_id'])+"")
        engine = db.engine.execute(rechatters_query)
        rechatter_schema = ReChatterSchema(many=True)
        rechatters = rechatter_schema.dump(engine)
        rechatters_data.append(rechatters)

    return jsonify({
        "data":chatters,
        "rechatter_data":rechatters_data
    })




def get_followed_users_chatters():
    my_id = request.args.get('my_id')
    chatters_query = text("SELECT *,(SELECT count(*) FROM like WHERE like.chatter_id=chatter.chatter_id) as likes_count,(SELECT count(*) FROM like where like.user_id="+str(my_id)+" and like.chatter_id=chatter.chatter_id) as is_liked,(SELECT count(*) FROM reply WHERE reply.chatter_id=chatter.chatter_id) as number_of_replies FROM chatter LEFT JOIN user on user.id=chatter.user_id LEFT JOIN follower on follower.followed_by="+str(my_id)+" WHERE chatter.user_id=follower.followed_user")
    engine = db.engine.execute(chatters_query)
    schema = ChatterSchema(many=True)
    chatters = schema.dump(engine)
    rechatters= None
    rechatters_data = []
    for chatter in chatters:
        rechatters_query = text("SELECT * FROM re_chatter LEFT JOIN chatter on chatter.chatter_id=re_chatter.original_chatter_id LEFT JOIN user on user.id=chatter.user_id WHERE re_chatter.r_chatter_id="+str(chatter['chatter_id'])+"")

        engine = db.engine.execute(rechatters_query)
        rechatter_schema = ReChatterSchema(many=True)
        rechatters = rechatter_schema.dump(engine)
        rechatters_data.append(rechatters)
        
    return jsonify({
        "data":chatters,
        "rechatter_data":rechatters_data
    })

def insert_Chatter():
    user_id = request.form.get('user_id')
    content = request.form.get('content')
    media =request.files.get('media')
    latlng = geo.latlng
    location_name = geo[0].__str__()
    media_type = request.form.get('media_type')
    category = request.form.get('category')
    new_chatter = None
    new_location = Location(name=location_name,longitude=latlng[1],latitude=latlng[0])
    db.session.add(new_location)
    db.session.commit()

    if media:
        is_saved,file_name = save_file(media, 'uploads')

        if is_saved:
            new_chatter = Chatter(category=category,user_id=user_id,chatter_content=content,location_id=new_location.location_id,media=file_name,media_type=media_type)
        else:
            return jsonify({
                "status":"Could not save file",
                "is_inserted": False
            })
    else:
        new_chatter = Chatter(category=category,user_id=user_id,chatter_content=content,location_id=new_location.location_id)
        
    db.session.add(new_chatter)
    db.session.commit()
    return jsonify({
        "status":"Successfully Inserted",
        "is_inserted": True
    })




def republish_Chatter():
    chatter_id = request.form.get('chatter_id')
    content = request.form.get('content')
    user_id = request.form.get('user_id')
    new_chatter = Chatter(user_id=user_id,chatter_content=content,chatter_publish_type='republished',)
    db.session.add(new_chatter)
    db.session.commit()

    republish_chatter = ReChatter(rechatter_user_id=user_id,original_chatter_id=chatter_id,r_chatter_id=new_chatter.chatter_id)
    db.session.add(republish_chatter)
    # new_chatter.original_chatter_id = republish_chatter.r_chatter_id
    db.session.commit()
    return jsonify({
        "status":"Inserted successfully",
        "is_inserted": True
    })




def delete_chatter():
    chatter_id = request.args.get('chatter_id')
    chatter = Chatter.query.get(chatter_id)
    
    if chatter.media:
        is_removed = remove_file(chatter.media, 'uploads')
        
        if is_removed == False:
            pass
        
    db.session.delete(chatter)
    db.session.commit()
    return jsonify({
        "status":"Deleted Successfully",
        "is_deleted":True
    })


def update_chatter():

    chatter_id = request.form.get('chatter_id')
    chatter_content = request.form.get('chatter_content')

    chatter = Chatter.query.filter_by(chatter_id=chatter_id).first()

    chatter.chatter_content = chatter_content
    db.session.commit()
    return jsonify({
        "is_updated":True,
        "status":"updated successfully"
    })

    



