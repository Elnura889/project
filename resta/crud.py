from sqlalchemy.orm import Session
import models, schemas

def get_user_by_login(db: Session, email:int)->Session.query:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_first_name(db: Session, user_first_name: str)->Session.query:
    return db.query(models.User).filter(models.User.user_fname == user_first_name).all()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.User).offset(skip).limit(limit).all()
    except Exception as e:
        print(f"Error in get_all_users: {e}")
        raise
def get_blog_by_id(db: Session, id: int)->Session.query:
    return db.query(models.Blog).filter(models.Blog.id == id).first()


def get_user_blogs(db: Session, user_id: int)->Session.query:
    return db.query(models.Blog).filter(models.Blog.author == user_id).all()


def get_all_blogs(db: Session, skip: int = 0, limit: int = 100)->Session.query:
    return db.query(models.Blogs).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate)->models.User:
    new_user = models.User(
                           first_name=user.first_name,
                           last_name=user.last_name,
                           username=user.username,
                           email=user.email,
                           password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_blog(db:Session, blog: schemas.BlogCreate, user_id)->models.Blog:
    new_blog = models.Blog(**blog.dict(), author=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def update_user(db: Session, email: str, user: schemas.UserUpdate) -> models.User:
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def update_blog(db: Session, blog_id: int, blog: schemas.BlogUpdate) -> models.Blog:
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog:
        for key, value in blog.dict().items():
            setattr(db_blog, key, value)
        db.commit()
        db.refresh(db_blog)
    return db_blog

def delete_user(db: Session, email: str) -> models.User:
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def delete_blog(db: Session, blog_id: int) -> models.Blog:
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
    return db_blog

