from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
#místrní soubory
from .. import models, schemas, utils
from ..database import engine, get_db
from ..schemas import UserCreate,UserOut #nějka se tomu nechtělo
from .. utils import hash
#jak sem dostat @app ? -. APIRouter

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(new_user : UserCreate,db: Session = Depends(get_db)):
    #hash 
    hashed_password=utils.hash(new_user.password)
    new_user.password=hashed_password
    user= models.User(**new_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user( id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exists")
    else:
        return user