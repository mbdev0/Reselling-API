from schemas import schemas
from auth import auth
from models.object_models import User, Storage
from operations import helper

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import List
from fastapi import HTTPException
import uuid

def create_storage(user_email:str,db:Session) -> Storage:
    user = get_user_by_email(user_email=user_email,db=db)
    db_storage = Storage(
    storageId = str(uuid.uuid4()),
    shoe_storage_space=schemas.StorageBase.__fields__['shoe_storage_space'].default,
    flips_storage_space=schemas.StorageBase.__fields__['flips_storage_space'].default,
    userid=user.userid
    )
    print(db_storage)
    db.add(db_storage)
    db.commit()
    db.refresh(db_storage)

    return db_storage

def get_user_storage(username:str, db:Session) -> Storage:
    user = get_user_by_username(username=username, db=db)
    storage = db.query(Storage).filter(Storage.userid == user.userid).first()
    if storage is None:
        raise HTTPException(status_code=404, detail=f'No storage was found for: {username}')
    return storage

def get_shoe_storage(username:str, db: Session):
    user = get_user_by_username(username=username, db=db)
    storage = db.query(Storage).filter(Storage.userid == user.userid).first()
    if storage is None:
        raise HTTPException(status_code=404, detail=f'Shoe Storage not found for: {username}')
    return storage.shoe_storage_space

def get_flips_storage(username:str, db: Session):
    user=get_user_by_username(username=username,db=db)
    storage = db.query(Storage).filter(Storage.userid == user.userid).first()
    if storage is None:
        raise HTTPException(status_code=404, detail=f'Flips Storage not found for: {username}')
    return storage.flips_storage_space

def add_shoe_to_storage(username:str, shoe:schemas.ShoeCreation, db:Session):
    storage = get_user_storage(username=username, db=db)
    shoe = shoe.__dict__
    shoe["id"] = str(uuid.uuid4())
    storage.shoe_storage_space['Shoes'].append(shoe) 
    new_product_on_stats(storage=storage, product=shoe, shoe=True)
    flag_modified(storage, "shoe_storage_space")
    db.add(storage)
    db.commit()

    return shoe

def add_flips_to_storage(username:str, item:schemas.FlipsCreation, db:Session):
    storage = get_user_storage(username=username,db=db)
    item = item.__dict__
    item['id'] = str(uuid.uuid4())
    storage.flips_storage_space['Flips'].append(item)
    new_product_on_stats(storage=storage, product=item, flip=True)
    flag_modified(storage, "flips_storage_space")
    db.add(storage)
    db.commit()


    return item

def get_flip_item_by_id(username:str, item_id:str, db:Session):
    storage = get_flips_storage(username=username, db=db)
    items = storage['Flips']
    for item in items:
        if item['id'] == item_id:
            return item
        
    raise HTTPException(status_code=404, detail=f'Item with id: {item_id} not found')

def get_shoe_item_by_id(username:str, shoe_id: str, db:Session):
    shoe_storage = get_shoe_storage(username=username, db=db)
    shoes = shoe_storage['Shoes']
    for shoe in shoes:
        if shoe['id'] == shoe_id:
            return shoe
    
    raise HTTPException(status_code=404, detail=f'Shoe with id: {shoe_id} not found')

def update_flip_item(username:str, item_id: str, item: schemas.Flips, db:Session):
    storage = get_user_storage(username=username,db=db)

    for it in storage.flips_storage_space['Flips']:
        if it['id'] == item_id:
            delete_product_stats(storage=storage, old_product=it, flip=True)
            for key,value in item.dict(exclude_unset=True).items():
                it[key] = value
            new_product_on_stats(storage=storage,product=it, flip=True)
            flag_modified(storage, "flips_storage_space")
            db.add(storage)
            db.commit()
            return it

    raise HTTPException(status_code=404, detail=f'Item with id: {item_id} not found')

def update_shoe_item(username:str, shoe_id: str, shoe: schemas.Shoe, db:Session):
    storage = get_user_storage(username=username,db=db)

    for it in storage.shoe_storage_space['Shoes']:
        if it['id'] == shoe_id:
            delete_product_stats(storage=storage, old_product=it, shoe=True)
            for key,value in shoe.dict(exclude_unset=True).items():
                it[key] = value
            new_product_on_stats(storage=storage, product=it,shoe=True)
            flag_modified(storage, "shoe_storage_space")
            db.add(storage)
            db.commit()
            return it

    raise HTTPException(status_code=404, detail=f'Shoe with id: {shoe_id} not found')

def delete_item_by_itemid(username:str ,item_id: str, deleteAllFlag: bool,db:Session):
    storage = get_user_storage(username=username, db=db)
    if deleteAllFlag:
        storage.flips_storage_space['Flips'] = []
        storage.flips_storage_space['Stats'] = schemas.StorageBase.__dict__['__fields__']['flips_storage_space'].default['Stats']
        flag_modified(storage,'flips_storage_space')
        db.add(storage)
        db.commit()
        return storage.flips_storage_space

    get_flip_item_by_id(username=username, item_id=item_id,db=db)
    for i,it in enumerate(storage.flips_storage_space['Flips']):
        if it['id'] == item_id:
            storage.flips_storage_space['Flips'].pop(i)
            delete_product_stats(storage=storage, old_product=it,flip=True)
            flag_modified(storage,"flips_storage_space")
            db.add(storage)
            db.commit()
            return storage.flips_storage_space

def delete_item_by_shoeid(username: str ,shoe_id: str, deleteAllFlag: bool ,db:Session):
    storage = get_user_storage(username=username, db=db)
    if deleteAllFlag:
        storage.shoe_storage_space['Shoes'] = []
        storage.shoe_storage_space['Stats'] = schemas.StorageBase.__dict__['__fields__']['shoe_storage_space'].default['Stats']
        flag_modified(storage,'shoe_storage_space')
        db.add(storage)
        db.commit()
        return storage.shoe_storage_space

    get_shoe_item_by_id(username=username, shoe_id=shoe_id,db=db)
    for i,it in enumerate(storage.shoe_storage_space['Shoes']):
        if it['id'] == shoe_id:
            storage.shoe_storage_space['Shoes'].pop(i)
            delete_product_stats(storage=storage, old_product=it,shoe=True)
            flag_modified(storage,"shoe_storage_space")
            db.add(storage)
            db.commit()
            return storage.shoe_storage_space
    
    raise HTTPException(status_code=404, detail='Code not founds')

def delete_product_stats(storage:Storage,old_product:dict = None, shoe: bool = False, flip: bool = False):

    if flip:
        helper.delete_product_stats_helper(storage.flips_storage_space['Stats'],old_product=old_product)
        
    elif shoe:
        helper.delete_product_stats_helper(storage.shoe_storage_space['Stats'],old_product=old_product)

def new_product_on_stats(storage:Storage,product:dict = None ,shoe: bool = False, flip: bool = False):

    if shoe:
        helper.new_product_stats_helper(current_stats=storage.shoe_storage_space.get('Stats'), new_product= product)
    elif flip:
        helper.new_product_stats_helper(current_stats=storage.flips_storage_space.get('Stats'), new_product=product)

def get_stats_for_flips(username:str, db:Session):
    storage = get_user_storage(username=username, db=db)
    return storage.flips_storage_space['Stats']

def get_stats_for_shoes(username:str, db:Session):
    storage = get_user_storage(username=username, db=db)
    return storage.shoe_storage_space['Stats']

def get_user_by_id(user_id:int,db:Session) -> User:
    get_by_id = db.query(User).filter(User.userid==user_id).first()
    if get_by_id is None:
        raise HTTPException(status_code=404, detail= f'User not found with the userid: {user_id}')

    return get_by_id

def get_user_by_email(user_email:str, db:Session) -> User:
    get_by_email = db.query(User).filter(User.email==user_email).first()
    if get_by_email is None:
        raise HTTPException(status_code=404, detail= f'User not found with the email: {user_email}')

    return get_by_email

def get_user_by_username(username:str, db:Session) -> User:
    get_by_username = db.query(User).filter(User.username==username).first()
    if get_by_username is None:
        raise HTTPException(status_code=404, detail= f'User not found with the username: {username}')

    return get_by_username

def get_all_users(db:Session) -> List[User]:
    get_users = db.query(User).all()
    if not get_users:
        raise HTTPException(status_code=404, detail = 'No users to be found')
    return get_users

def create_user(user:schemas.UserCreation, db:Session) -> dict:
    if db.query(User).filter(User.email==user.email).first():
        raise HTTPException(status_code=409, detail='Email already exists')
    if db.query(User).filter(User.username==user.username).first():
        raise HTTPException(status_code=409, detail = 'Username already exists')
    passhash = auth.hash_pass(user.password)
    db_user = User(userid=str(uuid.uuid4()),username=user.username, email=user.email,password=passhash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    create_storage(user_email=user.email,db=db)

    return schemas.User(username=db_user.username, email=db_user.email, userid=db_user.userid)

def update_user(username:str, db:Session, user:schemas.UserCreation) -> User:
    stored_user = get_user_by_username(username=username,db=db)
    user_update = user.dict(exclude_unset=True)
    for key,value in user_update.items():
        if key=='email':
            if db.query(User).filter(User.email==user.email).first():
                raise HTTPException(status_code=409, detail='Email already exists')
        if key == 'username':
            if db.query(User).filter(User.username==user.username).first():
                raise HTTPException(status_code=409, detail = 'Username already exists')

        if key == 'password':
            value = auth.hash_pass(password=value)
        setattr(stored_user,key,value)

    db.add(stored_user)
    db.commit()
    db.refresh(stored_user)

    return stored_user

def delete_user_by_username(username: str, db:Session) -> dict:
    user = get_user_by_username(username=username,db=db)
    db.delete(user)
    db.commit()

    return {'message':f'User with the details: {user.userid}, {user.username}, {user.email}, deleted succesfully'}

def delete_user_by_email(user_email:str, db:Session) -> dict:
    user = get_user_by_email(user_email=user_email, db=db)
    db.delete(user)
    db.commit()

    return {'message':f'User with the details: {user.userid}, {user.username}, {user.email}, deleted succesfully'}

