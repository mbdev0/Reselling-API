from pydantic import BaseModel
from typing import Union, Optional, Dict

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
    brand: str
    model: str
    quantity: int
    retail: float
    status: str
    resell: Optional[float]

class Shoe(Flips):
    colorway: str
    size: float
    Sku: Optional[str]


class StorageBase(BaseModel):
    shoe_storage_space = {"Shoes":[], "Stats": {}}
    flips_storage_space =  {"Flips":[], "Stats": {}}

class Storage(StorageBase):
    storageId:int
    userid:int

    class Config:
        orm_mode=True

