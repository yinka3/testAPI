
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db

router = APIRouter(
  prefix="/posts",
  tags=["Post"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int = 2, search: Optional[str] = ""):
  # posts = cursor.execute("SELECT * FROM posts").fetchall()

  results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, 
    models.Vote.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

  return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), curr_id: int = Depends(oauth2.get_current_user)):
  # new_post = cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
  #                          (new_post.title, new_post.content, new_post.published)).fetchone()
  # conn.commit()

  # print(curr_id.email)
  new_post = models.Post(user_id = curr_id.id, **new_post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)

  return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
  # post = cursor.execute(" SELECT * FROM posts WHERE id = (%s) ", (str(id),)).fetchone()

  post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, 
    models.Vote.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


  if not post:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail = f"post with id: {id} was not found")
  return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_id: int = Depends(oauth2.get_current_user)):
  # deleted_post = cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),)).fetchone()
  # conn.commit()

  deleted_post = db.query(models.Post).filter(models.Post.id == id)

  post = deleted_post.first()

  if not post:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail = f"post with id: {id} does not exist")

  if post.user_id != curr_id.id:
    raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                        detail=f"Not authorized to delete post")
  
  deleted_post.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db), curr_id: int = Depends(oauth2.get_current_user)):
  # post = cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
  #                       (post.title, post.content, post.published, (str(id)))).fetchone()
  # conn.commit()

  post_updated = db.query(models.Post).filter(models.Post.id == id)

  post = post_updated.first()

  if not post:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail = f"post with id: {id} does not exist")
  
  if post.user_id != curr_id.id:
    raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                        detail=f"Not authorized to update post")
  
  post_updated.update(new_post.model_dump(), synchronize_session=False)

  db.commit()
  
  return post_updated.first()