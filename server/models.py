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