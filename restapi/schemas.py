from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    body: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author: int

class UserBase(BaseModel):
    username: str
    email: str
class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    user_blogs: list[Post] = []