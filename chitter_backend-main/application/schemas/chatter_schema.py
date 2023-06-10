from application import ma

class ChatterSchema(ma.Schema):
    class Meta:
        fields = ('chatter_id','user_id','chatter_content','created_at','updated_at','media','location_id','chatter_publish_type','category','likes_count','original_chatter_id','id','username','profile_picture','is_liked','number_of_replies','number_of_chatters','media_type')