from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#Místní soubory
from .import models
from .database import engine
from .routers import posts,users,auth, votes
 
from . config import settings

models.Base.metadata.create_all(bind=engine)

origins=["*"] # jaké doméhy mohou přistupovat k api -> tedka všechny

app  =  FastAPI ()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
@app.get("/")
def root():
    return{"message":"Welcome to my api"}    

    


