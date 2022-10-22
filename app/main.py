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

@app.patch('/user/{user_id}', response_model=schemas.UserCreation)
def update_user(user_id: int, user: schemas.UserCreation, db: Session = Depends(interact_db)):
    return crud.update_user(user_id=user_id, user=user, db=db)

@app.delete('/user/{user_id}',response_model=dict)
def delete_user_by_id(user_id:int, db: Session = Depends(interact_db)):
    return crud.delete_user_by_id(user_id=user_id, db=db)

@app.get('/user/{user_id}/storage', response_model = schemas.Storage)
def get_storage_by_userid(user_id:int, db:Session = Depends(interact_db)):
    crud.get_stats_for_shoes(user_id=user_id,db=db)
    return crud.get_user_storage(user_id=user_id, db=db)

@app.get('/user/{user_id}/shoestorage')
def get_shoe_storage(user_id:int, db: Session = Depends(interact_db)):
    return crud.get_shoe_storage(user_id=user_id, db=db)

@app.get('/user/{user_id}/flipsstorage')
def get_flips_storage(user_id:int, db: Session = Depends(interact_db)):
    return crud.get_flips_storage(user_id=user_id, db=db)

@app.post('/user/{user_id}/shoestorage', response_model=schemas.ShoeCreation)
def add_shoe(user_id:int, shoe:schemas.Shoe, db: Session = Depends(interact_db)):
    return crud.add_shoe_to_storage(user_id=user_id, shoe=shoe, db=db)

@app.post('/user/{user_id}/flipsstorage', response_model=schemas.FlipsCreation)
def add_flip(user_id:int, flip:schemas.Flips, db: Session = Depends(interact_db)):
    return crud.add_flips_to_storage(user_id=user_id, item=flip, db=db)

@app.get("/user/{user_id}/flipstorage/{item_id}", response_model = schemas.FlipsCreation)
def get_flips_storage_item(user_id:int,item_id:str ,db: Session = Depends(interact_db)):
    return crud.get_flip_item_by_id(user_id=user_id,item_id=item_id,db=db)

@app.get("/user/{user_id}/shoestorage/{shoe_id}", response_model=schemas.ShoeCreation)
def get_shoe_storage_item(user_id:int,shoe_id:str ,db: Session = Depends(interact_db)):
    return crud.get_shoe_item_by_id(user_id=user_id, shoe_id=shoe_id, db=db)

@app.patch("/users/{user_id}/flipsstorage/{item_id}", response_model=schemas.FlipsCreation)
def update_item_by_id(user_id:int, item_id:str, item_updating:schemas.Flips ,db:Session = Depends(interact_db)):
    return crud.update_flip_item(user_id=user_id,item_id=item_id, item=item_updating, db=db)

@app.patch("/users/{user_id}/shoestorage/{shoe_id}", response_model=schemas.ShoeCreation)
def update_shoe_by_id(user_id:int, shoe_id: str, shoe: schemas.Shoe, db:Session = Depends(interact_db)):
    return crud.update_shoe_item(user_id=user_id,shoe_id=shoe_id, shoe=shoe, db=db)
    
@app.delete('/users/{user_id}/flipsstorage',response_model=dict)
def delete_item(user_id:int, item_id:Union[str,None]=None, deleteAll: bool = False,db:Session= Depends(interact_db)):
    return crud.delete_item_by_itemid(user_id=user_id, item_id=item_id, deleteAllFlag=deleteAll,db=db)

@app.delete('/users/{user_id}/shoestorage', response_model= list[schemas.ShoeCreation])
def delete_item(user_id:int, shoe_id:Union[str,None]=None, deleteAll: bool = False,db:Session= Depends(interact_db)):
    return crud.delete_item_by_shoeid(user_id=user_id, shoe_id=shoe_id, deleteAllFlag=deleteAll, db=db)

