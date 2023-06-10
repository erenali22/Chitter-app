from flask import Flask,Blueprint
from application.seeds import user

user_routes = Blueprint('user_route', __name__,static_folder='../static')


@user_routes.route('/register', methods=['POST'])
def Register():
    return user.register_user()


@user_routes.route('/login',methods=['POST'])
def Login():
    return user.login_user()


@user_routes.route('/get_all_users')
def GetAllUsers():
    return user.get_users()

@user_routes.route('/get_user')
def GetUser():
    return user.get_user()


@user_routes.route('/update_user',methods=['POST'])
def UpdateUser():
    return user.update_user()


@user_routes.route('/update_password',methods=['POST'])
def UpdatePassword():
    return user.change_password()