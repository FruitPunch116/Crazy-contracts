from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializeMixin
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData ( naming_convention={
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
} )

db = SQLAlchemy( metadata = metadata )

#--- HELPERS ---#


#--- USER ---#

class User ( db.Model, SerializeMixin ):
    __tablename__ = "users"
    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String, nullable =False )
    last_name = db.Column( db.String, nullable =False )
    email = db.Column( db.String, nullable =False )
    password = db.Column( db.String, nullable =False )
    username = db.Column( db.String, unique=True, nullable =False )

    contractor = db.reference( backref= "contractors" )

#--- CONTACTOR ---#

class Contractor ( db.Model, SerializeMixin ):
    __tablename__ = "contractors"
    id = db.Column( db.Integer, primary_key=True )
    company_name = db.Column( db.String )
    address = db.Column( db.String, nullable=False )
    secondary_address = db.Column( db.String )
    skills = db.Column( db.String, nullable=False )
    zip_code = db.Column( db.String, nullable=False )
    age = db.Column( db.Integer, nullable=False )

    user_id = db.relationship( "User" )

#--- SAVED ---#

class Saved ( db.Model, SerializeMixin ):
    __tablename__= "saved_posts"
    id = db.Column( db.Integer, primary_key=True )

    
#--- POST ---#

class Post ( db.Model, SerializeMixin ):
    __tablename__ = "posts"
    id = db.Column( db.Integer, primary_key=True )

    
#--- LIKES ---#

class Like ( db.Model, SerializeMixin ):
    __tablename__ = "likes"
    id = db.Column( db.Integer, primary_key=True )

    
#--- COMMENT ---#

class Comment ( db.Model, SerializeMixin ):
    __tablename__ = "comments"
    id = db.Column( db.Integer, primary_key=True )


#--- STAR ---#

class Star ( db.Model, SerializeMixin ):
    __tablename__ = "stars"
    id = db.Column( db.Integer, primary_key=True )

