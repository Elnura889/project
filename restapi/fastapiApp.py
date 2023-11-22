from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app =FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user=crud.get_user_by_login(db, email=user.email)

    if new_user:
        raise HTTPException(status_code=400, detail="Login is already taken by another user. Use another")
    return crud.create_user(db=db, user=user)

@app.post("/api/posts", response_model=schemas.Post)
def create_post(user_id:int, post: schemas.PostCreate, db: Session=Depends(get_db)):
    return crud.create_post(user_id=user_id, db=db, post=post)


@app.get("/api/users", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users

# getting user(s) by their first name
@app.get("/api/users/usernane/{user_username}", response_model=list[schemas.User])
def get_users_by_name(user_username, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_user_by_username(db=db, user_username=user_username)
    return users

# getting a user with a specific login which is unique
@app.get("/api/users/{email}", response_model=schemas.User)
def get_certain_user(email, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db, email)

# getting all blogs from db
@app.get("/api/posts", response_model=list[schemas.Post])
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_posts(db)

# getting a specific user's blogs
@app.get("/api/user/posts/{user_id}", response_model=list[schemas.Post])
def get_user_posts(user_id, db: Session = Depends(get_db)):
    return crud.get_user_posts(db, user_id)

# getting a certain blog by its id
@app.get("/api/post/{post_id}/", response_model=schemas.Post)
def get_post(post_id:int, db: Session = Depends(get_db)):
    return crud.get_post_by_id(db, post_id)


