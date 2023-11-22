from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150))
    userrname = Column(String(150))
    posts = relationship("Post", cascade="all, delete-orphan")

    def repr(self)->str:
        return f"User(id{self.id!r}, email={self.email!r}, password={self.password!r}, username={self.username!r})"

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    data = Column(String(10000))
    user_id = Column(Integer, ForeignKey('users.id'))
    post = relationship("User", back_populates="user_id")

    def repr(self)->str:
        return f"Post(id={self.id!r}), data={self.data!r}, user_id={self.user_id!r}, post={self.post!r})"