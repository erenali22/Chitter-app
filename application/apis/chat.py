from flask import Flask,Blueprint
from application.seeds import chat

chat_routes = Blueprint('chat_routes', __name__,static_folder='../static')


@chat_routes.route('/get_chats')
def GetChats():
    return chat.get_chats()
    
