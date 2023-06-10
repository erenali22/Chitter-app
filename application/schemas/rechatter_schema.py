from application import ma

class ReChatterSchema(ma.Schema):
    class Meta:
        fields = ('rechatter_id''original_chatter_id','r_chatter_id','original_chatter_id','rechatter_user_id','rechatter_created_at','rechatter_updated_at','chatter_content','user_id','media','media_type','chatter_id','username','profile_picture','id','created_at')