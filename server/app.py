#!/usr/bin/env python3

from models import db, User, Contractor, Review, Post, Like, Comment

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
    
@app.get(URL_PREFIX + "/reviews-section")
def get_reviews ():
    reviews = Review.query.all()
    response = [review.to_dict() for review in reviews]
    return jsonify(response), 200

@app.get(URL_PREFIX + "/posts-section")
def get_posts ():
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    return jsonify(response), 200

@app.get(URL_PREFIX + "/likes-section")
def get_likes ():
    likes = Like.query.all()
    response = [like.to_dict() for like in likes]
    return jsonify(response), 200

@app.get(URL_PREFIX + "/comments/info")
def get_comments ():
    comments = Comment.query.all()
    response = [comment.to_dict() for comment in comments]
    return jsonify(response), 200

@app.get(URL_PREFIX + "/saved-post/")
def  get_posts ():
    posts = Post.query.all()
    response = [post.to_dict() for post in Post]
    return jsonify(response), 200


if __name__ == ("__main__"):
    app.run (port=8001, debug=True)