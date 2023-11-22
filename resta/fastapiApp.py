from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.wsgi import WSGIMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user= crud.get_user_by_login(db, email=user.email)

    if new_user:
        raise HTTPException(status_code=400, detail="Login is already taken by another user. Use another")
    return crud.create_user(db=db, user=user)

# Retrieving all users
@app.get("/users/", response_model=schemas.User)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db=db, skip=skip, limit=limit)
    return users

# Fetching a specific user using their email
@app.get("/users/{email}", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    try:
        user = crud.get_user_by_email(db=db, email=email)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with email {email} not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Updating an existing user
@app.put("/users/{email}", response_model=schemas.User)
def update_user(email: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, email=email, user=user)

    if not updated_user:
        raise HTTPException(status_code=404, detail=f"User with email {email} not found")

    return updated_user

# Deleting a user
@app.delete("/users/{email}")
def delete_user(email: str, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db=db, email=email)

    if not deleted_user:
        raise HTTPException(status_code=404, detail=f"User with email {email} not found")

    return {"message": "User deleted successfully"}

@app.post("/api/blogs", response_model=schemas.Blog)
def create_blog(user_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = crud.create_blog(user_id=user_id, db=db, blog=blog)
    return new_blog


# Retrieving all blogs
@app.get("/api/blogs", response_model=schemas.Blog)
def get_all_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_all_blogs(db=db, skip=skip, limit=limit)
    return blogs



# Fetching a specific blog using its ID
@app.get("/api/blog/{blog_id}", response_model=schemas.Blog)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = crud.get_blog_by_id(db=db, blog_id=blog_id)

    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with ID {blog_id} not found")

    return blog



# Updating an existing blog
@app.put("/api/blog/{blog_id}", response_model=schemas.Blog)
def update_blog(blog_id: int, blog: schemas.BlogUpdate, db: Session = Depends(get_db)):
    updated_blog = crud.update_blog(db=db, blog_id=blog_id, blog=blog)

    if not updated_blog:
        raise HTTPException(status_code=404, detail=f"Blog with ID {blog_id} not found")

    return updated_blog



# Deleting a blog
@app.delete("/api/blog/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    deleted_blog = crud.delete_blog(db=db, blog_id=blog_id)

    if not deleted_blog:
        raise HTTPException(status_code=404, detail=f"Blog with ID {blog_id} not found")

    return {"message": "Blog deleted successfully"}








app.mount("/", WSGIMiddleware(app))


