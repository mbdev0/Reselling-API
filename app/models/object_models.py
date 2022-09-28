from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship, Session

from configuration.dbconfig import Base
from schemas import schemas

class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key = True, index=True)
    username = Column(String, unique = True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    storage = relationship("Storage", backref = 'users',uselist=False, cascade = 'all,delete,delete-orphan')

class Storage(Base):
    __tablename__ = 'user_storage'

    storageId = Column(Integer, primary_key = True, index=True)
    userid = Column(Integer, ForeignKey("users.userid"))
    shoe_storage_space = Column(JSON)
    flips_storage_space = Column(JSON)
