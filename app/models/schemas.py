from pydantic import BaseModel, Json


class UserBase(BaseModel):
    username: str 
    
class UserCreation(UserBase):
    email:str
    password:str

class User(UserBase):
    user_id: int
    shoe_storage_id: int
    flips_storage_id: int

class StorageBase(BaseModel):
    flips_storage: Json
    shoe_storage: Json

class StorageCreation(StorageBase):
    pass

class Storage(StorageBase):
    user_id:int
    storage_id:int

