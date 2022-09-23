from models import object_models, crud
from fastapi import Depends, FastAPI, HTTPException
from configuration.dbconfig import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

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

@app.post("/user", response_model=schemas.UserCreation)
def create_user(user: schemas.UserCreation, db: Session = Depends(interact_db)):
    if crud.get_user_by_email(user_email=user.email, db=db):
        raise HTTPException(status_code=409, detail='Email already exists')
    if crud.get_user_by_username(username=user.username, db=db):
        raise HTTPException(status_code=409, detail='Username already exists')

    return crud.create_user(db=db,user=user)

@app.get("/users", response_model=List[schemas.User])
def get_all_users(db:Session = Depends(interact_db)):
    get_users = crud.get_all_users(db=db)
    if not get_users:
        raise HTTPException(status_code=404, detail = 'No users to be found')
    return get_users

@app.get('/user/{user_id}', response_model = schemas.User)
def get_user_by_id(user_id:int, db: Session = Depends(interact_db)):
    get_by_id = crud.get_user_by_id(user_id=user_id, db=db)
    if get_by_id is None:
        raise HTTPException(status_code = 404, detail= f'No user was found with the id: {user_id}')

    return get_by_id 


