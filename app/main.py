from models import object_models
from operations import crud
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from configuration.dbconfig import engine, interact_db
from sqlalchemy.orm import Session
from typing import List, Union
from datetime import timedelta
from schemas import schemas
from auth import auth 
from auth import authconfig
object_models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def response():
    return({'message':'welcome'})

@app.post("/token", response_model=schemas.Token, tags=['Token'])
def login(formdata: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(interact_db)):
    user = auth.validate_user(formdata=formdata, db=db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail='Invalid Credentials',
            headers= {'WWW-Authentication':'Bearer'}
        )
    access_token = auth.create_acess_token({'sub':user.username},expiry_delta=timedelta(minutes=authconfig.ACCESS_TOKEN_EXPIRY_MINS))
    return schemas.Token(access_token=access_token,token_type='Bearer')

@app.post("/user", response_model=schemas.User, tags=['User'])
def create_user(user: schemas.UserCreation, db: Session = Depends(interact_db)):
    return crud.create_user(db=db,user=user)

@app.get("/users", response_model=List[schemas.User], tags=['User'])
def get_all_users(
    db:Session = Depends(interact_db),
    currUser = Depends(auth.current_user)):

    if currUser.superuser:
        return crud.get_all_users(db=db)
    
    raise HTTPException(status_code=401, detail='Unauthorized',headers={'WWW-Authenticate':'Bearer'})

@app.get('/{username}', response_model = schemas.User, tags=['User'])
def get_user_by_id(username:str,currUser: schemas.User = Depends(auth.current_user) ,db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.get_user_by_username(username=username, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.get_user_by_username(username=username, db=db)

@app.patch('/{username}', response_model=schemas.User, tags=['User'])
def update_user(
    username: str, 
    user: schemas.UserCreation, 
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.update_user(username=username, user=user, db=db)
    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.update_user(username=username, user=user, db=db)

@app.delete('/{username}',response_model=dict, tags=['User'])
def delete_user_by_username(
    username:str,
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.delete_user_by_username(username=username, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.delete_user_by_username(username=username, db=db)

@app.get('/{username}/storage', response_model = schemas.Storage, tags=['Storage'])
def get_storage_by_username(
    username:str,
    currUser:schemas.User = Depends(auth.current_user),
    db:Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.get_user_storage(username=username, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.get_user_storage(username=username, db=db)

@app.get('/{username}/shoestorage',response_model=schemas.Shoes_Storage, tags=['Shoe Storage'])
def get_shoe_storage(
    username:str,
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.get_shoe_storage(username=username, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.get_shoe_storage(username=username, db=db)

@app.get('/{username}/flipsstorage',response_model=schemas.Flips_Storage, tags=['Flips Storage'])
def get_flips_storage(
    username:str,
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.get_flips_storage(username=username, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.get_flips_storage(username=username, db=db)

@app.post('/{username}/shoestorage', response_model=schemas.ShoeCreation, tags=['Shoe Storage'])
def add_shoe(
    username:str,
    shoe:schemas.Shoe,
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.add_shoe_to_storage(username=username, shoe=shoe, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.add_shoe_to_storage(username=username, shoe=shoe, db=db)

@app.post('/{username}/flipsstorage', response_model=schemas.FlipsCreation, tags=['Flips Storage'])
def add_flip(
    username:str, 
    flip:schemas.Flips,
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.add_flips_to_storage(username=username, item=flip, db=db)

    auth.check_if_currUser(currUser=currUser,username=username)
    return crud.add_flips_to_storage(username=username, item=flip, db=db)

@app.get("/{username}/flipstorage/{item_id}", response_model = schemas.FlipsCreation, tags= ['Flips Storage'])
def get_flips_storage_item(
    username:str,
    item_id:str, 
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.get_flip_item_by_id(username=username,item_id=item_id,db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.get_flip_item_by_id(username=username,item_id=item_id,db=db)

@app.get("/{username}/shoestorage/{shoe_id}", response_model=schemas.ShoeCreation, tags=['Shoe Storage'])
def get_shoe_storage_item(
    username:str,
    shoe_id:str,
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.get_shoe_item_by_id(username=username, shoe_id=shoe_id, db=db)

    auth.check_if_currUser(currUser=currUser,username=username)
    return crud.get_shoe_item_by_id(username=username, shoe_id=shoe_id, db=db)

@app.patch("/{username}/flipsstorage/{item_id}", response_model=schemas.FlipsCreation, tags=['Flips Storage'])
def update_item_by_id(
    username:str, 
    item_id:str, 
    item_updating:schemas.Flips,
    currUser:schemas.User = Depends(auth.current_user),
    db:Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.update_flip_item(username=username,item_id=item_id, item=item_updating, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.update_flip_item(username=username,item_id=item_id, item=item_updating, db=db)

@app.patch("/{username}/shoestorage/{shoe_id}", response_model=schemas.ShoeCreation, tags=['Shoe Storage'])
def update_shoe_by_id(
    username:str, 
    shoe_id: str, 
    shoe: schemas.Shoe,
    currUser:schemas.User = Depends(auth.current_user),
    db:Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.update_shoe_item(username=username,shoe_id=shoe_id, shoe=shoe, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.update_shoe_item(username=username,shoe_id=shoe_id, shoe=shoe, db=db)
    
@app.delete('/{username}/flipsstorage',response_model=schemas.Flips_Storage, tags=['Flips Storage'])
def delete_flip(
    username:str, 
    item_id:Union[str,None]=None, 
    deleteAll: bool = False,
    currUser:schemas.User = Depends(auth.current_user),
    db:Session= Depends(interact_db)):

    if currUser.superuser:
        return crud.delete_item_by_itemid(username=username, item_id=item_id, deleteAllFlag=deleteAll,db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.delete_item_by_itemid(username=username, item_id=item_id, deleteAllFlag=deleteAll,db=db)

@app.delete('/{username}/shoestorage', response_model= schemas.Shoes_Storage, tags=['Shoe Storage'])
def delete_shoe(
    username:str, 
    shoe_id:Union[str,None]=None, 
    deleteAll: bool = False,
    currUser:schemas.User = Depends(auth.current_user),
    db:Session= Depends(interact_db)):

    if currUser.superuser:
        return crud.delete_item_by_shoeid(username=username, shoe_id=shoe_id, deleteAllFlag=deleteAll, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.delete_item_by_shoeid(username=username, shoe_id=shoe_id, deleteAllFlag=deleteAll, db=db)

