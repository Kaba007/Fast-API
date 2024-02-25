from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from sqlalchemy import func
#místrní soubory
from .. import models, schemas, oauth2
from ..database import engine, get_db
from ..schemas import UserCreate,UserOut,PostResponse,PostCreate, PostOUT , Postdetails, CommentIn,CommandOUT #nějka se tomu nechtělo
from .. oauth2 import get_current_user

router=APIRouter(
    prefix="/comments" ,## Přičitá se k URL
    tags=["comments"]
)

#Create comment
@router.post("/{id}",status_code=status.HTTP_201_CREATED,response_model=CommandOUT)
def create_comment(id:int, comment:CommentIn, db: Session =Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_exists= db.query(models.Post.id==id).first()
    
    if post_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"comment with the id {id} was not found")
    
    new_comment=models.Comment(user_id=current_user.id ,post_id=id, **comment.dict())
    db.add(new_comment)
    db.commit() #JAKO conn.commit
    return CommandOUT(
        id=new_comment.id,
        ts=new_comment.ts)

#update command

#delete command
@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_exists = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    
    comment_exists = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.post_id == post_id).first()
    if comment_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id {comment_id} was not found")

    db.delete(comment_exists)
    db.commit()
