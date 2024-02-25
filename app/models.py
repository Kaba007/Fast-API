from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__= "users"
    email = Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    ts = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Comment(Base):
    __tablename__= "comments"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    post_id= Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True,nullable=False)
    user_id =Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), primary_key=True,nullable=False)
    content=Column(String(100),nullable=False)
    ts = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)    
    post = relationship("Post", back_populates="comments") 
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)  # Předpokládá, že 'published' je Boolean
    ts = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    owner = relationship("User") # NENÍ sql vazba, vrací user informace do JSON odpovědi
    comments = relationship("Comment", back_populates="post")

class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), primary_key=True,nullable=False)
    dir = Column(Integer,nullable=False)
    

