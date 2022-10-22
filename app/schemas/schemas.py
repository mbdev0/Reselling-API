from pydantic import BaseModel, conint, confloat
from typing import Union, Optional, Literal
from uuid import UUID

class UserBase(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
  
class UserCreation(UserBase):
    password:str

    class Config:
        orm_mode=True
            
class User(UserBase):
    userid: Union[str, None] = None

    class Config:
        orm_mode=True

class Flips(BaseModel):
    brand: Optional[str]
    model: Optional[str]
    quantity: Optional[conint(gt=0)]
    retail: Optional[confloat(gt=0)]
    status: Optional[Literal['NOT LISTED', 'LISTED', 'PACKED', 'SHIPPED']]
    resell: Optional[confloat(ge=0)]

class FlipsCreation(Flips):
    id:UUID

class Shoe(Flips):
    colorway: Optional[str]
    size: Optional[confloat(gt=0)]
    Sku: Optional[str]

class ShoeCreation(Shoe):
    id:UUID

class StorageBase(BaseModel):
    shoe_storage_space = {"Shoes":[], "Stats": {
            "total_retail":0, "total_resell":0, "current_net": 0, "total_quantity":0, "amount_not_listed":0, "amount_listed":0,
            "amount_packed":0,"amount_shipped":0
            }
        }
    flips_storage_space =  {"Flips":[], "Stats": {
            "total_retail":0, "total_resell":0, "current_net": 0, "total_quantity":0, "amount_not_listed":0, "amount_listed":0,
            "amount_packed":0,"amount_shipped":0
            }
        }

class Storage(StorageBase):
    storageId:int
    userid:int

    class Config:
        orm_mode=True

