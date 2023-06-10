from flask import Flask,Blueprint
from application.seeds import follower

follower_routes = Blueprint('follower_routes', __name__,static_folder='../static')

@follower_routes.route('/get_following_users')
def GetFollowers():
    return follower.get_followed_users()

@follower_routes.route('/get_my_followers')
def GetMyFollowers():
    return follower.get_my_followers()

@follower_routes.route('/get_another_user_followers')
def GetAnotherUserFollowers():
    return follower.get_another_user_followers()

@follower_routes.route('/get_another_user_followings')
def GetAnotherUserFollowings():
    return follower.get_another_user_followings()


@follower_routes.route('/follow_user',methods=['POST'])
def FollowUser():
    return follower.follow_user()


@follower_routes.route('/unfollow_user',methods=['DELETE'])
def UnFollowUser():
    return follower.unfollow_user()
