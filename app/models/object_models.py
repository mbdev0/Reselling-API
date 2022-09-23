from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship, Session

from configuration.dbconfig import Base
from schemas.schemas import *

class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key = True, index=True)
    username = Column(String, unique = True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    storage = relationship("Storage", back_populates = 'users',uselist=False)

    @classmethod
    def create_user(db: Session, user: UserCreation):
        print('hello')

    """
    Create a user 
    Get by user id
    Get by user email
    Get a users storage ID
    Update a users email
    update a users password
    delete a user by id
    delete a user by email
    """
    

class Storage(Base):
    __tablename__ = 'user_storage'

    storageId = Column(Integer, primary_key = True, index=True)
    userId = Column(Integer, ForeignKey("users.userid"))
    shoe_storage_space = Column(JSON)
    flips_storage_space = Column(JSON)
    
    user = relationship("User", back_populates = 'storage')

    """
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
