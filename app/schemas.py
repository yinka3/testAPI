from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationError, conint


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True

class UserRes(BaseModel):
    id: int
    email: EmailStr
    createdUser_at: datetime

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostCreate(BasePost):
    pass

class Post(BasePost):
    id: int
    created_at: datetime 
    user_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: int

    def __validate__(self):
        if self.dir not in (0, 1):
            raise ValidationError("dir must be 0 or 1")