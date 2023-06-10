from flask import Flask,Blueprint
from application.seeds import reply

reply_routes = Blueprint('reply_routes', __name__,static_folder='../static')


@reply_routes.route('/insert_reply',methods=['POST'])
def InsertReply():
    return reply.insert_reply()

@reply_routes.route('/get_replies')
def GetReplies():
    return reply.get_replies()

@reply_routes.route('/delete_reply',methods=['DELETE'])
def DeleteReply():
    return reply.delete_reply()



@reply_routes.route('/update_reply',methods=['PUT'])
def UpdateReply():
    return reply.update_reply()