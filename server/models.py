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



#-----  Users  -----#
class User ( db.Model ) :
    __tablename__ = "users"
    # Create table columns
    id = db.Column (db.Integer, primary_key = True, unique = True)
    name = db.Column (db.String, nullable = False)
    last_name = db.Column (db.String, nullable = False)
    e_mail = db.Column (db.String, nullable = False)
    password = db.Column (db.String, nullable = False)
    zip_code = db.Column (db.Integer, nullable = False)

    # Establish one-to-one relationship with the contractors
    contractor = db.relationship ("Contractor", back_populates = "user")
    # Establish many-to-many relationship with the review table
    reviews_transmitted = db.relationship ("Review", back_populates = "transmitter")
    reviews_received = db.relationship ("Review", back_populates =  "receptor")

    # Create the association between the reviews and the contractors thru users 
    reviews_transmitted_text = association_proxy ("reviews_transmitted", "text")
    reviews_transmitted_stars = association_proxy ("reviews_transmitted", "stars")
    reviews_received_text = association_proxy ("reviews_received", "text")
    reviews_received_stars = association_proxy ("reviews_received", "stars")

#-----  Contractors  -----#
class Contractor ( db.Model ) :
    # Gives the table a name
    __tablename__ = "contractors"
    # Create table columns
    id = db.Column (db.Integer, primary_key = True, unique = True)
    company_name = db.Column (db.String, nullable = False)
    address = db.Column (db.String)
    secondary_address = db.Column (db.String)
    specialty = db.Column (db.String)
    skills = db.Column (db.String, nullable = False)
    age = db.Column (db.Integer, nullable = False)

    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"), unique = True)
    # Establish one-to-one relationship with the users table
    user = db.relationship ("User", back_populates = "contractor")

#-----  Reviews  -----#
class Review ( db.Model ) :
    # Gives the table a name
    __tablename__ = "reviews"
    # Create table columns
    id = db.Column (db.Integer, primary_key = True, unique = True)
    stars = db.Column (db.Integer, nullable = False)
    text = db.Column (db.String, nullable = False)

    transmitter_id = db.Column (db.Integer, db.ForeignKey ("users.id"))
    receptor_id = db.Column (db.Integer, db.ForeignKey ("users.id"))

    # Establish many-to-many relationship with the user table
    transmitter = db.relationship ("User", back_populates = "reviews_transmitted")
    receptor = db.relationship ("User", back_populates="reviews_received")
    
#-----  Posts  -----#
class Post ( db.Model ) :
    # Gives the table a name
    __tablename__ = "posts"
    id = db.Column (db.Integer, primary_key = True, unique = True)
    # image = db.Column (db.Blob, nullable = False)

    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"))

#-----  Likes  -----#
class Like ( db.Model ) :
    # Gives the table a name
    __tablename__ = "likes"
    # Create table columns
    id = db.Column (db.Integer, primary_key = True)

    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"))
    post_id = db.Column (db.Integer, db.ForeignKey ("posts.id"))

#-----  Comments  -----#
class Comment ( db.Model ) :
    # Gives the table a name
    __tablename__ = "comments"
    # Create table columns
    id = db.Column (db.Integer, primary_key = True, unique = True)
    body = db.Column (db.String)
    
    post_id = db.Column (db.Integer, db.ForeignKey ("posts.id"))
    user_id = db.Column (db.Integer, db.ForeignKey ("users.id"))


#-----    -----#
