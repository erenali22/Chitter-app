from flask import request,Blueprint,jsonify
from application import db
from application.models.reply import Reply
from application.schemas.reply_schema import ReplySchema
from sqlalchemy import text

def insert_reply():
    user_id = request.form.get('user_id')
    chatter_id = request.form.get('chatter_id')
    reply_content = request.form.get('content')

    new_reply = Reply(user_id=user_id,chatter_id=chatter_id,reply_content=reply_content)
    db.session.add(new_reply)
    db.session.commit()
    return jsonify({
        "status":"Inserted successfully",
        "is_inserted": True
    })


def get_replies():
    chatter_id = request.args.get('chatter_id')
    replies_query = text("SELECT * FROM reply LEFT JOIN user on user.id=reply.user_id WHERE chatter_id="+str(chatter_id))
    engine = db.engine.execute(replies_query)
    reply_schema = ReplySchema(many=True)
    replies=reply_schema.dump(engine)
    return jsonify({
        "data":replies
    })

def delete_reply():
    reply_id = request.args.get('reply_id')
    reply = Reply.query.get(reply_id)
    db.session.delete(reply)
    db.session.commit()
    return jsonify({
        "status":"deleted successfully",
        "is_deleted": True
    })

def update_reply():
    reply_id  = request.form.get('reply_id')
    reply = Reply.query.get(reply_id)
    content = request.form.get('content')

    reply.reply_content = content
    db.session.commit()
    return jsonify({
        "is_updated":True,
        "status":"Reply Updated Successfully"
    })
