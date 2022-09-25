from models import object_models, crud
from fastapi import Depends, FastAPI, HTTPException
from configuration.dbconfig import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List, Union

from schemas import schemas

object_models.Base.metadata.create_all(bind=engine)

def interact_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def response():
    return({'message':'welcome'})

@app.post("/user", response_model=dict)
def create_user(user: schemas.UserCreation, db: Session = Depends(interact_db)):
    return crud.create_user(db=db,user=user)

@app.get("/users", response_model=List[schemas.User])
def get_all_users(db:Session = Depends(interact_db)):
    return crud.get_all_users(db=db)

@app.get('/user/{user_id}', response_model = schemas.User)
def get_user_by_id(user_id:int, db: Session = Depends(interact_db)):
    return crud.get_user_by_id(user_id=user_id, db=db)

@app.patch('/user/{user_id}', response_model=schemas.User)
def update_user(user_id: int, user: schemas.User, db: Session = Depends(interact_db)):
    return crud.update_user(user_id=user_id, user=user, db=db)


