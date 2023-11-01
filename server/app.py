#!/usr/bin/env python3

from models import db, User, Contractor, Post

from flask import Flask, jsonify, request, session
# from flask_cors import CORS
from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = b'm~\xb6E6\x8b\xe9\xf0\x9d\xa7\x81\x8b\x91&aC\xc1\x7f\xe1\x11\xecn\xeeW\xa1\xf6vT\x96\xb9N\x0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate (app, db)

db.init_app(app)

URL_PREFIX = "/api/v1/admin"

@app.route("/")
def index ():
    return "<h1>Welcome to the contractors favorite website</h1>"

@app.get(URL_PREFIX + "/users")
def get_users ():
    users = User.query.all()
    response = [user.to_dict() for user in users]

    return jsonify(response), 200

@app.get(URL_PREFIX + "/contractors/info")
def get_contractors ():
    contractors = Contractor.query.all()
    response = [contractor.to_dict() for contractor in contractors]
    
    return jsonify(response), 200

"""    
@app.get(URL_PREFIX + "/reviews-section")
def get_reviews ():
    "<h4>REVIEWS route</h4>"
    reviews = Review.query.all()
    response = [review.to_dict() for review in reviews]
    return jsonify(response), 200"""

@app.get(URL_PREFIX + "/posts-section")
def get_posts ():
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    
    return jsonify(response), 200

"""@app.get(URL_PREFIX + "/likes-section")
def get_likes ():
    "<h4>LIKES route</h4>"
    likes = Like.query.all()
    response = [like.to_dict() for like in likes]
    return jsonify(response), 200"""

"""@app.get(URL_PREFIX + "/comments/info")
def get_comments ():
    "<h4>COMMENTS route</h4>"
    comments = Comment.query.all()
    response = [comment.to_dict() for comment in comments]
    return jsonify(response), 200"""


"""@app.get(URL_PREFIX + "/saved-post/")
def  get_posts ():
    "<h4SAVED POSTS route></h4>"
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    return jsonify(response), 200"""

@app.get(URL_PREFIX + "/user/<int:id>")
def get_user_id (id):
    try:
        user = User.query.filter(User.id == id).first()
        return jsonify(user.to_dict()), 200
    except:
        return ({"error": "Episode not found"}), 404

@app.post (URL_PREFIX + "/new-user")
def create_user ():
    data = request.json
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    print(data)
    return new_user.to_dict(), 201

@app.delete(URL_PREFIX + "/users/<int:id>")
def delete_user (id):
    user = User.query.filter(User.id == id).first()
    db.session.delete(user)
    db.session.commit()
    return {}, 204    
    
@app.patch(URL_PREFIX + "/user-edit/<int:id>")
def edit_user(id):
    data = request.json
    print(data)
    User.query.filter(User.id == id).update(data)
    user = User.query.filter(User.id == id).first()
    
    db.session.add(user)
    db.session.commit()
    
    return user.to_dict(),200

"""
creating serialize rules for the route (what to show on the browser when the API load)
# self.to_dict(rules=("-contractor.address",))
"""

if __name__ == ('__main__'):
    app.run (port=8001, debug=True)