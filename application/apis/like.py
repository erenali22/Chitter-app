from flask import Flask,Blueprint
from application.seeds import like

like_routes = Blueprint('like_routes', __name__,static_folder='../static')



@like_routes.route('/like_chatter',methods=['POST'])
def LikeChatter():
    return like.like_chatter()

@like_routes.route('/unlike_chatter',methods=['POST'])
def UnlikeChatter():
    return like.unlike_chatter()
    