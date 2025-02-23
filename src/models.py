import os
import sys
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column,Integer,String,Date, ForeignKey
from eralchemy2 import render_er
Base = declarative_base()

# Tabla Usuarios
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50),unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=True)
    bio = Column(String(255), nullable=True)
    create_at = Column(Date, nullable=False)
    
    #
    post = relationship('Post', backref='author')
    followers = relationship('Follower', backref='user', foreign_keys='Follower.user_id')
    following = relationship('Follower', backref='follower', foreign_keys='Follower.follower_id')

# Tabla Publicaciones
class Post(Base):
    __tablename__= 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    img_url = Column(String(255), nullable=False)
    caption = Column(String(255), nullable=True)
    post_at = Column(Date, nullable=False)

    # Relaciones
    likes = relationship('Like', backref='post')
    comments = relationship('Comment', backref='post')

# Tabla Comentarios
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    posts_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    text = Column(String(255), nullable=False)
    comment_at = Column(Date, nullable=False)

# Tabla Likes
class Like(Base):
    __tablename__ = 'likes' 
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    liked_at = Column(Date, nullable=False)
# Tabla Seguidores
class Follower(Base):
    __tablename__ = 'followers'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followed_at = Column(Date, nullable=False)

# Tabla Direct mensajes
class DirectMessage(Base):
    __tablename__ = 'direct_messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String(255), nullable=False)
    sent_at = Column(Date, nullable=False)

# class Person(Base):
#     __tablename__ = 'person'
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(nullable=False)

# class Address(Base):
#     __tablename__ = 'address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id: Mapped[int] = mapped_column(primary_key=True)
#     street_name: Mapped[str]
#     street_number: Mapped[str]
#     post_code: Mapped[str] = mapped_column(nullable=False)

#     def to_dict(self):
#         return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
