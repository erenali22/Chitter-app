from flask import Flask
from config import DATABASE_URI,SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from flask_socketio import SocketIO, send,emit

app = Flask(__name__)


app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ma= Marshmallow(app)
db = SQLAlchemy(app)
Migrate(app,db)
CORS(app)
socketIo = SocketIO(app, cors_allowed_origins="*")

from application.seeds.message import send_message,get_messages
from application.seeds.chat import get_chats


@socketIo.on('connect')
def connect(info):
    print("Connected")
    return None

@socketIo.on('send_message')
def SendMessage(data):
    print("send")
    print(data)
    send_message(data['sender_id'], data['receiver_id'], data['message'])
    emit('receive_messages',data,broadcast=True)
    emit('receive_contacts',data,broadcast=True)
    return None


@socketIo.on('need_receive_contacts')
def ReceiveContacts(data):
    emit('receive_contacts',data)
    return None



from application.apis.user import user_routes
app.register_blueprint(user_routes,url_prefix='/apis/user')

from application.apis.reply import reply_routes
app.register_blueprint(reply_routes,url_prefix='/apis/reply')


from application.apis.message import message_routes
app.register_blueprint(message_routes,url_prefix='/apis/message')

from application.apis.like import like_routes
app.register_blueprint(like_routes,url_prefix='/apis/like')


from application.apis.follower import follower_routes
app.register_blueprint(follower_routes,url_prefix='/apis/follow')


from application.apis.chatter import chatter_routes
app.register_blueprint(chatter_routes,url_prefix='/apis/chatter')


from application.apis.chat import chat_routes
app.register_blueprint(chat_routes,url_prefix='/apis/chat')
