from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
class UserCreate(BaseModel):
    email: EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email: EmailStr
    
    class Config:
        from_attributes = True
       

class UserLogin(BaseModel):
    email:EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    class Config:
        from_attributes = True

class PostCreate(PostBase):
    pass
    

class PostResponse(PostBase): #převzato z PostBase
    id: int
    ts : datetime
    user_id : int
    owner : UserOut
    class Config:
        from_attributes = True ### ZMĚNA z orm_mode na from_attributes

class PostOUT(BaseModel):
    Post:PostResponse
    votes:int
    class Config:
        from_attributes = True


class Token(BaseModel):
    acces_token : str
    token_type : str

class TokenData(PostBase):
    id : Optional[str]=None
    title: Optional[str] = None
    content: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir : int 