from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

metadata = MetaData ( naming_convention = {
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq" : "uq_%(table_name)s_%(column_0_name)s",
    # "uq" : "ck_%(table_name)s_%(constraint_name)s",
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata = metadata)



#----- Users -----#
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    e_mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)

    contractor = db.relationship("Contractor", back_populates="user")

    reviews_transmitted = db.relationship("Review", foreign_keys="Review.transmitter_id", back_populates="transmitter")
    reviews_received = db.relationship("Review", foreign_keys="Review.receptor_id", back_populates="receptor")

    posts = db.relationship("Post", back_populates="user")

    likes = db.relationship("Like", back_populates="user")

    comments = db.relationship("Comment", back_populates="user")

    saved_post = db.relationship("Saved_Post", back_populates="user")

    reviews_transmitted_text = association_proxy("reviews_transmitted", "text")
    reviews_transmitted_stars = association_proxy("reviews_transmitted", "stars")
    reviews_received_text = association_proxy("reviews_received", "text")
    reviews_received_stars = association_proxy("reviews_received", "stars")

    serialize_rules = (
        "-reviews_transmitted.transmitter",
        "-reviews_received.receptor",
        "-contractor.user",
        "-posts.user",
        "-comments.user",
    )

#----- Contractors -----#
class Contractor(db.Model, SerializerMixin):

    __tablename__ = "contractors"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    company_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    secondary_address = db.Column(db.String)
    specialty = db.Column(db.String)
    skills = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    user = db.relationship("User", back_populates="contractor")

    post = db.relationship("Post", back_populates="contractor")

    serialize_rules = ("-user.contractor",)

#----- Reviews -----#
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    stars = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=False)

    transmitter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    receptor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    transmitter = db.relationship("User", back_populates="reviews_transmitted", foreign_keys=[transmitter_id])
    receptor = db.relationship("User", back_populates="reviews_received", foreign_keys=[receptor_id])

    serialize_rules = ("-transmitter.reviews_transmitted", "-receptor.reviews_received",)

#----- Posts -----#
class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # image = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    contractor_id = db.Column(db.Integer, db.ForeignKey("contractors.id"))

    user = db.relationship("User", back_populates="posts")
    contractor = db.relationship("Contractor", back_populates="post")

    comments = db.relationship("Comment", back_populates="post")
    likes = db.relationship("Like", back_populates="post")

    comment_text = association_proxy("comments", "body")

    serialize_rules = ("-user.posts", "-comments.post")

#----- Likes -----#
class Like(db.Model, SerializerMixin):

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    user = db.relationship("User", back_populates="likes")
    post = db.relationship("Post", back_populates="likes")

#----- Comments -----#
class Comment(db.Model, SerializerMixin):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    body = db.Column(db.String)

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="comments")
    post = db.relationship("Post", back_populates="comments")

    serialize_rules = ("-user.comments", "-post.comments")

#----- Saved -----#
class Saved_Post(db.Model, SerializerMixin):

    __tablename__ = "saved"
    id = db.Column(db.Integer, primary_key=True, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    user = db.relationship("User", back_populates="saved_post")