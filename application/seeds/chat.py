from flask import  request,jsonify
from application import db
from flask import request
from application.models.message import Message
from application.schemas.message_schema import MessageSchema
from application.models.chat import Chat
from application.schemas.chat_schema import ChatSchema
from sqlalchemy import text


def get_chats():
    my_id = request.args.get('my_id')
    chats_sql = text("SELECT * FROM chat LEFT JOIN user on user.id=chat.user_id WHERE  chat.created_for="+str(my_id))
    engine = db.engine.execute(chats_sql)
    chats_schema = ChatSchema(many=True)
    chats = chats_schema.dump(engine)
    
    return jsonify({'data':chats})


def insert_chat(receiver_id,sender_id):
    new_chat1 = Chat(created_for=receiver_id,user_id=sender_id)
    new_chat2 = Chat(created_for=sender_id,user_id=receiver_id)

    check_chat1 = Chat.query.filter_by(created_for=sender_id,user_id=receiver_id).first()
    check_chat2 = Chat.query.filter_by(created_for=receiver_id,user_id=sender_id).first()

    if not check_chat2:
        db.session.add(new_chat2)
    
    if not check_chat1:
        db.session.add(new_chat1)


    db.session.commit()