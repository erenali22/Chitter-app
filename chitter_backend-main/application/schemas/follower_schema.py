from application import ma

class FollowerSchema(ma.Schema):
    class Meta:
        fields = ('follower_p_id','followed_user','followed_by','timestamp','id','username','profile_picture','is_followed')