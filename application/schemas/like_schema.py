from application import ma

class LikeSchema(ma.Schema):
    class Meta:
        fields = ('like_id','user_id','chatter_id','timestamp','id','username','profile_picture')