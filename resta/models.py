from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    user_blogs = relationship("Blog", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self)->str:
        return f"User(user_id{self.user_id!r}, name={self.first_name!r}, lastname={self.last_name!r}, username={self.username!r})"

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(String(255), nullable=False)
    blog_author = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    author = relationship("User", back_populates="user_blogs")

    def __repr__(self)->str:
        return f"Blog(id={self.id!r}), title={self.title!r}, body={self.body!r}, author={self.blog_author!r})"