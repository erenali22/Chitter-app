from application import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','username','email','password','profile_picture','bio','location','created_at','updated_at','is_followed','number_of_followers','number_of_following','number_of_chatters','chatter_publish_type','intrests')