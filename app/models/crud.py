from schemas import schemas
from sqlalchemy.orm import Session
from models.object_models import User, Storage
from typing import List
from fastapi import HTTPException

"""
For STORAGE
    get shoe storage
    get flips storage
    add an item to shoe storage
    add an item to flips storage
    update an items -> any of its dict keys
    delete an item from storage
    delete an item from flips storage
    clear the inventory -> flips and storage -> or either or
    get total amount of retail for shoe or flips -> or both
    get net profit (resell-retail) for shoe or flips -> or both
"""

def create_storage(user_email:str,db:Session) -> Storage:
    user = get_user_by_email(user_email=user_email,db=db)
    print(user.userid)
    db_storage = Storage(shoe_storage_space={},flips_storage_space={},userId=user.userid)
    db.add(db_storage)
    db.commit()
    db.refresh(db_storage)

    return db_storage
    
"""
For USERS
    Create a user  x
    Get by user id x
    Get by user email x
    get user by username x
    a users storage needs to be created on sign up -> show too x
    Get a users storage ID 
    Update a users email x
    update a users password x
    delete a user by id
    delete a user by email 
"""
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

def update_user(user_id:int, db:Session, user:schemas.User) -> User:
    stored_user = get_user_by_id(user_id=user_id, db=db)
    user_update = user.dict(exclude_unset=True)
    print(user_update)
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