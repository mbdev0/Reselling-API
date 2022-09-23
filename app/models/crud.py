from schemas import schemas
from sqlalchemy.orm import Session
from models.object_models import User, Storage
from typing import List


"""
For USERS
    Create a user 
    Get by user id
    Get by user email
    get user by username
    Get a users storage ID
    Update a users email
    update a users password
    delete a user by id
    delete a user by email 
"""
def get_user_by_id(user_id:int,db:Session) -> User:
    return db.query(User).filter(User.userid==user_id).first()

def get_user_by_email(user_email:str, db:Session) -> User:
    return db.query(User).filter(User.email==user_email).first()

def get_user_by_username(username:str, db:Session) -> User:
    return db.query(User).filter(User.username==username).first()

def get_all_users(db:Session) -> List[User]:
    return db.query(User).all()

def create_user(user:schemas.UserCreation, db:Session) -> User:
    fake_hash = user.password+'fake_hash'
    db_user = User(username=user.username, email=user.email,password=fake_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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