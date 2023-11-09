#!/usr/bin/env python3

from models import db, User, Contractor, Post, Review, Comment

from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = b'm~\xb6E6\x8b\xe9\xf0\x9d\xa7\x81\x8b\x91&aC\xc1\x7f\xe1\x11\xecn\xeeW\xa1\xf6vT\x96\xb9N\x0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

cors = CORS(app, resources={r"/api/*/admin": {"origins": "*"}})

bcrypt = Bcrypt(app)

migrate = Migrate (app, db)

db.init_app(app)

URL_PREFIX = "/api/v1/admin"

@app.route(URL_PREFIX + "/")
def index ():
    page = f"""
    <h1>Welcome to the contractors favorite's website API.</h1>
    <p>Here you can find the routes for the different path of the <strong>Application Programming Interface</strong> 
    or known as well as <strong>API</strong>.\nIn order to navigate the API the main <strong>URL</strong> you will need is going to depend.
    \nIf your site still in development mode the require URL is going to be <strong>localhost</strong> plus the application site port number.
    \nFor example the one  we are using on this project is: <strong>http://localhost:8001{URL_PREFIX}</strong> or <strong>http://127.0.0.1:8001{URL_PREFIX}</strong>.\n
    Those numbers are referencing to the localhost URL.</p>\n<p>In case the website's backend is deployed you can go directly to the specific website</p>
    <br>
    <h1>Here are some of the endpoints that you can use to get information from the different routes</h1>
    <h2>Getting the users overall info:</h2>
    <a href="http://localhost:8001{URL_PREFIX}/users">http://localhost:8001{URL_PREFIX}/users</a>
    <h2>Getting a specific user information:</h2>
    <a href="http://localhost:8001{URL_PREFIX}/user/5">http://localhost:8001{URL_PREFIX}/user/<int:id></a>
    <h2>Getting the contractors overall info:</h2>
    <a href="http://localhost:8001{URL_PREFIX}/contractors/info">http://localhost:8001{URL_PREFIX}/contractors/info</a>
    <h2>Getting a specific contractor information:</h2>
    <a href="http://localhost:8001{URL_PREFIX}/contractors/info/1">http://localhost:8001/{URL_PREFIX}/contractors/info/<int:id></a>
    """
    return page

# -- User section -- #

@app.get(URL_PREFIX + "/users")
def get_users ():
    users = User.query.all()
    response = [user.to_dict() for user in users]

    return jsonify(response), 200

@app.get(URL_PREFIX + "/user/<int:id>")
def get_user_id (id):
    try:
        user = User.query.filter(User.id == id).first()
        return jsonify(user.to_dict()), 200
    except:
        return ({"error": "User not found"}), 404

@app.post (URL_PREFIX + "/new-user")
def create_user ():
    """data = request.json
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    # print(data)
    return new_user.to_dict(), 201"""

    try:
        data = request.json
        print(data)
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(
            name=data['name'],
            last_name=data["last_name"],
            e_mail=data["e_mail"],
            password=password_hash,
            zip_code=data["zip_code"]
        )
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id

        return new_user.to_dict(), 201
    except Exception as e:
        return { 'error': str(e) }, 406

@app.delete(URL_PREFIX + "/user-delete/<int:id>")
def delete_user (id):
    user = User.query.filter(User.id == id).first()

    for contractor in user.contractor:
        db.session.delete(contractor)

    for post in user.posts:
        db.session.delete(post)

    for comment in user.comments:
        db.session.delete(comment)

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
    
    return user.to_dict(),204

#  -- Contractors section -- #

@app.get(URL_PREFIX + "/contractors/info")
def get_contractors ():
    contractors = Contractor.query.all()
    response = [contractor.to_dict() for contractor in contractors]
    
    return jsonify(response), 200

@app.get(URL_PREFIX + "/contractor/info/<int:id>")
def get_contractor_id (id):
    try:
        contractor = Contractor.query.filter(Contractor.id == id).first()
        return jsonify(contractor.to_dict()), 200
    except:
        return ({"Error": "Contractor not found in the database"})
   
@app.post(URL_PREFIX + "/new-contractor")
def create_contractor ():
    data = request.json
    print(data)
    new_contractor = Contractor(**data)
    db.session.add(new_contractor)
    db.session.commit()
    return new_contractor.to_dict(), 201

@app.patch(URL_PREFIX + "/contractor/info/edit/<int:id>")
def edit_contractor (id):
    data = request.json
    print(data)
    Contractor.query.filter(Contractor.id == id).update(data)
    contractor = Contractor.query.filter(Contractor.id == id).first()

    db.session.add(contractor)
    db.session.commit()

    return contractor.to_dict(),204

# -- Reviews section -- #
@app.get(URL_PREFIX + "/reviews-section")
def get_reviews ():
    "<h4>REVIEWS route</h4>"
    reviews = Review.query.all()
    response = [review.to_dict() for review in reviews]
    return jsonify(response), 200

@app.get(URL_PREFIX + "/review/<int:id>")
def get_review_id (id):
    review = Review.query.filter(Review.id == id).first()
    return jsonify(review.to_dict()),200

@app.post(URL_PREFIX + "/new-review")
def create_review ():
    data = request.json
    print(data)
    new_review = Review(**data)

    db.session.add(new_review)
    db.session.commit()

    return new_review.to_dict(), 201

@app.patch(URL_PREFIX + "/edit-review/<int:id>")
def edit_review (id):
    data = request.json
    Review.query.filter(Review.id == id).update(data)
    review = Review.query.filter(Review.id == id).first()

    db.session.add(review)
    db.session.commit()

    return review.to_dict(),204

@app.get(URL_PREFIX + "/posts-section")
def get_posts ():
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    
    return jsonify(response), 200

@app.get(URL_PREFIX + "/post/<int:id>")
def get_post_id (id):
    post = Post.query.filter(Post.id == id).first()
    return jsonify(post.to_dict()),200

@app.post(URL_PREFIX + "/new-post")
def create_post ():
    data = request.json
    print(data)
    new_post = Post(**data)

    db.session.add(new_post)
    db.session.commit()

    return new_post.to_dict(),201

@app.patch(URL_PREFIX + "/edit-post/<int:id>")
def edit_post (id):
    data = request.json()
    Post.query.filter(Post.id == id).update(data)
    post = Post.query.filter(Post.id == id).first()

    db.session.add(post)
    db.session.commit()

    return post.to_dict(),204

#  -- Post section -- #
@app.delete(URL_PREFIX + "/delete/post/<int:id>")
def delete_post (id):
    post = Post.query.filter(Post.id == id).first()

    db.session.delete(post)
    db.session.commit()

    return {},204

"""@app.get(URL_PREFIX + "/likes-section")
def get_likes ():
    "<h4>LIKES route</h4>"
    likes = Like.query.all()
    response = [like.to_dict() for like in likes]
    return jsonify(response), 200"""


# -- Comments section -- #
@app.get(URL_PREFIX + "/comments/info")
def get_comments ():
    "<h4>COMMENTS route</h4>"
    comments = Comment.query.all()
    response = [comment.to_dict() for comment in comments]
    return jsonify(response), 200

@app.get(URL_PREFIX + "/comment/info/<int:id>")
def get_comment_id (id):
    comment = Comment.query.filter(Comment.id == id).first()
    return jsonify(comment.to_dict()),200

@app.post(URL_PREFIX + "/create-comment")
def create_comment ():
    data = request.json
    print(data)
    new_comment = Comment(**data)
    
    db.session.add(new_comment)
    db.session.commit()

    return new_comment.to_dict(),201

@app.patch(URL_PREFIX + "/edit-comment/<int:id>")
def edit_comment (id):
        data = request.json
        Comment.query.filter(Comment.id == id).update(data)
        comment = Comment.query.filter(Comment.id == id).first()

        db.session.add(comment)
        db.session.commit()

        return comment.to_dict(),200

@app.delete(URL_PREFIX + "/delete/comment/<int:id>")
def delete_comment (id):
    comment = Comment.query.filter(Comment.id == id).first()

    db.session.delete(comment)
    db.session.commit()

    return {},204

"""@app.get(URL_PREFIX + "/saved-post/")
def  get_posts ():
    "<h4SAVED POSTS route></h4>"
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    return jsonify(response), 200"""   
    
"""
creating serialize rules for the route (what to show on the browser when the API load)
# self.to_dict(rules=("-contractor.address",))
"""

if __name__ == ('__main__'):
    app.run (port=8001, debug=True)