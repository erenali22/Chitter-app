from flask import  request,jsonify
from application import db
from flask import request
from application.models.message import Message
from application.schemas.message_schema import MessageSchema
from application.models.chat import Chat
from application.seeds import chat
from application.schemas.chat_schema import ChatSchema
from sqlalchemy import text





def send_message(sender_id,receiver_id,message_content):
   
    
    
    chat.insert_chat(receiver_id, sender_id)

   
    new_message  = Message(message_content=message_content,receiver_id=receiver_id,sender_id=sender_id)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({
        "is_inserted": True,
        "stats":"successly inserted",
    })

def get_messages(): 
    chat_id = request.args.get('chat_id')
    chat = Chat.query.get(chat_id)

    messages_query = text("SELECT * FROM message LEFT JOIN user on user.id=message.sender_id WHERE message.receiver_id="+str(chat.created_for)+" AND message.sender_id="+str(chat.user_id)+" OR message.receiver_id="+str(chat.user_id)+" AND message.sender_id="+str(chat.created_for))
    engine = db.engine.execute(messages_query)
    schama = MessageSchema(many=True)
    messages = schama.dump(engine)
    return jsonify({
        "data":messages

    })



