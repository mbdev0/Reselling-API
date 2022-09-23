from pydantic import BaseModel, Json, validator

class UserBase(BaseModel):
    username: str 
    
class UserCreation(UserBase):
    email:str
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
    userid: int

    class Config:
        orm_mode=True

class StorageBase(BaseModel):
    flips_storage: Json
    shoe_storage: Json

class StorageCreation(StorageBase):
    pass

class Storage(StorageBase):
    storage_id:int
    user_id:int

    class Config:
        orm_mode=True

