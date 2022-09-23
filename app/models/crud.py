from schemas import schemas
from sqlalchemy.orm import Session
from models.object_models import User, Storage


"""
For USERS
    Create a user 
    Get by user id
    Get by user emai
    Get a users storage ID
    Update a users email
    update a users password
    delete a user by id
    delete a user by email 
"""
def create_user(user:schemas.UserCreation, db:Session):
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