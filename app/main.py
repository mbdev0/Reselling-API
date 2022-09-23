from models import object_models,crud
from fastapi import Depends, FastAPI, HTTPException
from configuration.dbconfig import engine, SessionLocal
from sqlalchemy.orm import Session

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
    
    return crud.create_user(db=db,user=user)


