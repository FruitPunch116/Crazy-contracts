from flask_sqlachemy import SQLAlchemy
from sqlalchemy import Metadata
from sqlalchemy_serializer import SerializeMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

metadata = Metadata ( naming_convention = {
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq" : "uq_%(table_name)s_%(column_0_name)s",
    "uq" : "ck_%(table_name)s_%(constraint_name)s",
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata = metadata)


id = db.Column (db.Integer, primary_key = True)

#-----  Users  -----#
class User ( db.Model ) :
    __tablename__ = "users"
    id
    name = db.Column (db.String, nullable = False)
    last_name = db.Column (db.String, nullable = False)
    e_mail = db.Column (db.String, nullable = False)
    password = db.Column (db.String, nullable = False)
    zip_code = db.Column (db.Integer, nullable = False)

#-----  Contractors  -----#
class Contractor ( db.Model ) :
    __tablename__ = "contractors"
    id
    company_name = db.Column (db.String, nullable = False)
    address = db.Column (db.String)
    secondary_address = db.Column (db.String)
    specialty = db.Column (db.String)
    skills = db.Column (db.String, nullable = False)
    age = db.Column (db.Integer, nullable = False)