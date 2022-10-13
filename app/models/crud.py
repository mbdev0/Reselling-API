from schemas import schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from models.object_models import User, Storage
from typing import List
from fastapi import HTTPException
import uuid

"""
For STORAGE
    get shoe storage x 
    get flips storage x 
    add an item to shoe storage x
    add an item to flips storage x
    update an items -> any of its dict keys e.g price, quantity, etc
    delete an item from storage
    delete an item from flips storage
    clear the inventory -> flips and storage -> or either or
    get total amount of retail for shoe or flips -> or both
    get net profit (resell-retail) for shoe or flips -> or both
"""

def create_storage(user_email:str,db:Session) -> Storage:
    user = get_user_by_email(user_email=user_email,db=db)
    db_storage = Storage(shoe_storage_space={"Shoes":[],"Stats":{}},flips_storage_space={"Items":[],"Stats":{}},userid=user.userid)
    db.add(db_storage)
    db.commit()
    db.refresh(db_storage)

    return db_storage

def get_user_storage(user_id:int, db:Session) -> Storage:
    storage = db.query(Storage).filter(Storage.userid == user_id).first()
    if storage is None:
        raise HTTPException(status_code=404, detail=f'No storage was found for the user id: {user_id}')
    return storage

def get_shoe_storage(user_id:int, db: Session):
    storage = db.query(Storage).filter(Storage.userid == user_id).first()
    if storage is None:
        return HTTPException(status_code=404, detail=f'Shoe Storage not found for user: {user_id}')
    return storage.shoe_storage_space

def get_flips_storage(user_id:int, db: Session):
    storage = db.query(Storage).filter(Storage.userid == user_id).first()
    if storage is None:
        return HTTPException(status_code=404, detail=f'Flips Storage not found for user: {user_id}')
    return storage.flips_storage_space

def add_shoe_to_storage(user_id:int, shoe:schemas.ShoeCreation, db:Session):
    storage = get_user_storage(user_id=user_id,db=db)
    shoe = shoe.__dict__
    shoe["id"] = str(uuid.uuid4())
    storage.shoe_storage_space['Shoes'].append(shoe) 
    flag_modified(storage, "shoe_storage_space")
    db.add(storage)
    db.commit()

    return shoe

def add_flips_to_storage(user_id:int, item:schemas.FlipsCreation, db:Session):
    storage = get_user_storage(user_id=user_id,db=db)
    item = item.__dict__
    item['id'] = str(uuid.uuid4())
    storage.flips_storage_space['Items'].append(item)
    flag_modified(storage, "flips_storage_space")
    db.add(storage)
    db.commit()

    return item

def get_flip_item_by_id(user_id:int, item_id:str, db:Session):
    storage = get_flips_storage(user_id=user_id,db=db)
    items = storage['Items']
    for item in items:
        if item['id'] == item_id:
            return item
        
    return HTTPException(status_code=404, detail=f'Item with id: {item_id} not found')

def get_shoe_item_by_id(user_id:int, shoe_id: str, db:Session):
    shoe_storage = get_shoe_storage(user_id=user_id, db=db)
    shoes = shoe_storage['Shoes']
    for shoe in shoes:
        if shoe['id'] == shoe_id:
            return shoe
    
    return HTTPException(status_code=404, detail=f'Shoe with id: {shoe_id} not found')

def update_flip_item(user_id:int, item_id: str, item: schemas.Flips, db:Session):
    flip_item = get_flip_item_by_id(user_id=user_id, item_id=item_id,db=db)
    flip_item_update = item.dict(exclude_unset=True)

    for key,value in flip_item_update.items():
        setattr(flip_item, key, value)
    
    db.add(flip_item)
    db.commit()
    db.refresh(flip_item)

    return flip_item

def get_user_by_id(user_id:int,db:Session) -> User:
    get_by_id = db.query(User).filter(User.userid==user_id).first()
    if get_by_id is None:
        raise HTTPException(status_code = 404, detail= f'No user was found with the id: {user_id}')
    return get_by_id

def get_user_by_email(user_email:str, db:Session) -> User:
    return db.query(User).filter(User.email==user_email).first()

def get_user_by_username(username:str, db:Session) -> User:
    return db.query(User).filter(User.username==username).first()

def get_all_users(db:Session) -> List[User]:
    get_users = db.query(User).all()
    if not get_users:
        raise HTTPException(status_code=404, detail = 'No users to be found')
    return get_users

def create_user(user:schemas.UserCreation, db:Session) -> dict:
    if get_user_by_email(user_email=user.email, db=db):
        raise HTTPException(status_code=409, detail='Email already exists')
    if get_user_by_username(username=user.username, db=db):
        raise HTTPException(status_code=404, detail = 'Username already exists')
    fake_hash = user.password+'fake_hash'
    db_user = User(username=user.username, email=user.email,password=fake_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    storage=create_storage(user_email=user.email,db=db)

    resp= {
        "username":db_user.username,
        "email":db_user.email,
        "password":db_user.password,
        "storage": {
            "shoe_storage_space":storage.shoe_storage_space,
            "flips_storage_space":storage.flips_storage_space
        }
    }

    return resp

def update_user(user_id:int, db:Session, user:schemas.UserCreation) -> User:
    stored_user = get_user_by_id(user_id=user_id, db=db)
    user_update = user.dict(exclude_unset=True)
    for key,value in user_update.items():
        setattr(stored_user,key,value)

    db.add(stored_user)
    db.commit()
    db.refresh(stored_user)

    return stored_user

def delete_user_by_id(user_id: int, db:Session) -> dict:
    user = get_user_by_id(user_id=user_id, db=db)
    db.delete(user)
    db.commit()

    return {'message':f'User with the details: {user.userid}, {user.username}, {user.email}, deleted succesfully'}

def delete_user_by_email(user_email:str, db:Session) -> dict:
    user = get_user_by_email(user_email=user_email, db=db)
    db.delete(user)
    db.commit()

    return {'message':f'User with the details: {user.userid}, {user.username}, {user.email}, deleted succesfully'}

