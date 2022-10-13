from pydantic import BaseModel
from typing import Union, Optional, Dict

# Do i want the id's to be automatically generated from here or not
from uuid import UUID

class UserBase(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
  
class UserCreation(UserBase):
    password:str

    class Config:
        orm_mode=True

# To be used later
    # @validator('email')
    # def check_none_email(cls,c):
    #     if c is None:
    #         raise ValueError('Email = None')
    #     return c
    
    # @validator('password')
    # def check_none_pass(cls,c):
    #     if c is None:
    #         raise ValueError('Pass is none')
            
class User(UserBase):
    userid: Union[str, None] = None

    class Config:
        orm_mode=True

class Flips(BaseModel):
    brand: Optional[str]
    model: Optional[str]
    quantity: Optional[int]
    retail: Optional[float]
    status: Optional[str]
    resell: Optional[float]

class FlipsCreation(Flips):
    id:UUID

class Shoe(Flips):
    colorway: Optional[str]
    size: Optional[float]
    Sku: Optional[str]

class ShoeCreation(Shoe):
    id:UUID

class StorageBase(BaseModel):
    shoe_storage_space = {"Shoes":[], "Stats": {}}
    flips_storage_space =  {"Flips":[], "Stats": {}}

class Storage(StorageBase):
    storageId:int
    userid:int

    class Config:
        orm_mode=True

