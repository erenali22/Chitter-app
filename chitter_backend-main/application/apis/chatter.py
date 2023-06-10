from flask import Flask,Blueprint
from application.seeds import chatter

chatter_routes = Blueprint('chatter_routes', __name__,static_folder='../static')

@chatter_routes.route('/get_chatters')
def GetChatters():
    return chatter.get_Chatters()


@chatter_routes.route('/get_followed_users_chatters')
def GetFollowedUsersChatters():
    return chatter.get_followed_users_chatters()

@chatter_routes.route('/insert_chatter',methods=['POST'])
def InsertChatter():
    return chatter.insert_Chatter()



@chatter_routes.route('/republish_chatter',methods=['POST'])
def RepublishChatter():
    return chatter.republish_Chatter()



@chatter_routes.route('/delete_chatter',methods=['DELETE'])
def DeleteChatter():
    return chatter.delete_chatter()


@chatter_routes.route('/update_chatter',methods=['PUT'])
def UpdateChatter():
    return chatter.update_chatter()