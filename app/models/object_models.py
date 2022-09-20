from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from configuration.dbconfig import Base

class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key = True, index=True)
    username = Column(String, unique = True, index=True)
    password = Column(String)

    storage = relationship("Storage", back_populates = 'user')


class Storage(Base):
    __tablename__ = 'user_storage'

    storageId = Column(Integer, primary_key = True, index=True)
    storage_space = Column(JSON)

    user = relationship("User", back_populates = 'storage')
