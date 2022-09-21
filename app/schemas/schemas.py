from pydantic import BaseModel, Json

class UserBase(BaseModel):
    username: str 
    
class UserCreation(UserBase):
    email:str
    password:str

class User(UserBase):
    user_id: int
    storage_id: int

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

