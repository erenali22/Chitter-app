from flask import Flask,Blueprint
from application.seeds import message

message_routes = Blueprint('message_routes', __name__,static_folder='../static')

@message_routes.route('/send_message',methods=['POST'])
def SendMessage():
    return message.send_message()

@message_routes.route('/get_messages')
def GetMessages():
    return message.get_messages()


