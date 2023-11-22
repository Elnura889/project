from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    body: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass
class Blog(BlogBase):
    id: int
    author: int

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    user_id: int
    user_blogs: list[Blog] = []

class BlogUpdate(BlogBase):
    pass

class BlogDelete(BaseModel):
    pass

class UserDelete(BaseModel):
    pass


