from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

metadata = MetaData ( naming_convention = {
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq" : "uq_%(table_name)s_%(column_0_name)s",
    "uq" : "ck_%(table_name)s_%(constraint_name)s",
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata = metadata)



#-----  Users  -----#
class User ( db.Model ) :
    __tablename__ = "users"
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String, nullable = False)
    last_name = db.Column (db.String, nullable = False)
    e_mail = db.Column (db.String, nullable = False)
    password = db.Column (db.String, nullable = False)
    zip_code = db.Column (db.Integer, nullable = False)

#-----  Contractors  -----#
class Contractor ( db.Model ) :
    __tablename__ = "contractors"
    id = db.Column (db.Integer, primary_key = True)
    company_name = db.Column (db.String, nullable = False)
    address = db.Column (db.String)
    secondary_address = db.Column (db.String)
    specialty = db.Column (db.String)
    skills = db.Column (db.String, nullable = False)
    age = db.Column (db.Integer, nullable = False)

    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"))

#-----  Reviews  -----#
class Review ( db.Model ) :
    __tablename__ = "reviews"
    id = db.Column (db.Integer, primary_key = True)
    stars = db.Column (db.Integer, nullable = False)
    text = db.Column (db.String, nullable = False)

    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"))
    contractor_id = db.Column (db.Integer, db.ForeignKey ("contractors.id"))

#-----  Posts  -----#
class Post ( db.Model ) :
    __tablename__ = "posts"
    id = db.Column (db.Integer, primary_key = True)
    image = db.Column (db.Blob, nullable = False)

    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"))

#-----  Likes  -----#
class Like ( db.Model ) :
    __tablename__ = "likes"
    id = db.Column (db.Integer, primary_key = True)

    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"))
    post_id = db.Column (db.Integer, db.ForeignKey ("posts.id"))

#-----  Comments  -----#
class Comment ( db.Model ) :
    __tablename__ = "comments"
    id = db.Column (db.Integer, primary_key = True)
    body = db.Column (db.String)
    
    post_id = db.Column (db.Integer, db.ForeignKey ("posts.id"))
    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"))


#-----    -----#
