from application import ma

class ChatSchema(ma.Schema):
    class Meta:
        fields = ('chat_id','user_id','created_for','created_at','id','username','profile_picture')