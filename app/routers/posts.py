from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from sqlalchemy import func
#místrní soubory
from .. import models, schemas, oauth2
from ..database import engine, get_db
from ..schemas import UserCreate,UserOut,PostResponse,PostCreate, PostOUT #nějka se tomu nechtělo
from .. oauth2 import get_current_user
#jak sem dostat @app ? -. APIRouter

router=APIRouter(
    prefix="/posts" ,## Přičitá se k URL
    tags=["Posts"]
)
#, 
@router.get("/",response_model=List[schemas.PostOUT])
def get_posts(db: Session = Depends(get_db) ,response_model=PostResponse,current_user: int = Depends(oauth2.get_current_user), 
              limit : int =10, skip :int =0, search :Optional[str]=""):
    #Tak jak by to dělal normální člověk
    #cursor.execute("""Select * from posts""")
    #posts=cursor.fetchall()s
    #demdence přes sql alchemy
    
    #Omezení pouze na vlastní posts
    #posts=db.query(models.Post).filter(models.Post.user_id==current_user.id).all()
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return post

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=PostResponse,)
def create_post(post: PostCreate ,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)) :
    #Tak jak by to dělal normální člověk
    #cursor.execute("""INSERT INTO posts(title,content,published) VALUES( %s,%s,%s)  RETURNING * """,(post.title,post.content,post.published))
    
    #new_post=cursor.fetchone() #Ukončí SQL příkaz
    
    #conn.commit() ### potvrdí změnu do DB -. bacha je to metoda -. msí mít ()!!!

    #demdence přes sql alchemy¨
  
  
    
    new_post = models.Post(user_id=current_user.id,**post.dict()) # Převeden na slovkík a naváže na data do insert
    db.add(new_post)
    db.commit() #JAKO conn.commit
    db.refresh(new_post) # abxhc vrátil co jsem zapsal -> JAKO RETURNING *

    return new_post

# title str, contetn string

@router.get("/{id}", response_model=PostOUT)
def get_post(id: int, db: Session = Depends(get_db),response_model=PostResponse,current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""Select * from posts where id= %s """,(str(id),))  # validuje jako int, pak musím převést na string, nehrozí zneužití -> nejdřív jako int -. až tady v kodu jedu jako str
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id== id).first()

    post = post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id== id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found")
    
    #Omezení pouze na určité posts
    #if post.user_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "Not authorized to performe requested action") 

    return post





@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""Delete from posts where id=%s RETURNING *""",(str(id),))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    post_querry = db.query(models.Post).filter(models.Post.id == id)
    
    post= post_querry.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found")
   
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "Not authorized to performe requested action") 
    
    post_querry.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

     

@router.put("/{id}")
def update_post(id : int, updated_post: PostCreate,db: Session = Depends(get_db),response_model=PostResponse,current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""update posts  set title=%s,content=%s, published=%s where id=%s RETURNING *""",(post.title,post.content,post.published,str(id),))
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "Not authorized to performe requested action") 
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()