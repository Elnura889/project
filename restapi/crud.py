from sqlalchemy.orm import Session
import models, schemas

def get_user_by_login(db: Session, email:str)->Session.query:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_first_name(db: Session, user_first_name: str)->Session.query:
    return db.query(models.User).filter(models.User.user_fname == user_first_name).all()


def get_all_users(db: Session, skip: int = 0, limit: int = 100)->Session.query:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_post_by_id(db: Session, id: int)->Session.query:
    return db.query(models.Post).filter(models.Post.id == id).first()


def get_user_posts(db: Session, user_id: int)->Session.query:
    return db.query(models.Post).filter(models.Post.post == user_id).all()


def get_all_posts(db: Session, skip: int = 0, limit: int = 100)->Session.query:
    return db.query(models.Post).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate)->models.User:
    new_user = models.User(
                           email=user.email,
                           password=user.password,
                           username=user.username)
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_post(db:Session, post: schemas.PostCreate, user_id)->models.Post:
    new_post = models.Post(**post.dict(), post=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post