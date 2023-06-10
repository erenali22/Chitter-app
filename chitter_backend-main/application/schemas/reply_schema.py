from application import ma

class ReplySchema(ma.Schema):
    class Meta:
        fields = ('reply_id','reply_content','chitter_id','user_id','chatter_id','created_at','updated_at','id','username','profile_picture')