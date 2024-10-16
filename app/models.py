from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String, nullable = False)
    genre = Column(String, nullable = False)
    ott_release = Column(Boolean, server_default= 'True', nullable = False)
    rating = Column(Integer)
    created_at = Column(TIMESTAMP, server_default = text('now()'), nullable = False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable = False)
    owner = relationship('User')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP, server_default = text('now()'), nullable = False)

class Vote(Base):
    __tablename__= 'votes'
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable= False, primary_key= True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False, primary_key= True)