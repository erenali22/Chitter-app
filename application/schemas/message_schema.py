from application import ma
class MessageSchema(ma.Schema):
    class Meta:
        fields = ('message_id','sender_id','receiver_id','message_content','created_at','id','username','profile_picture')
