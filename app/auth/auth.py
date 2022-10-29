from operations import crud
from auth import authconfig

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError


def hash_pass(password:str) -> str:
    return authconfig.passcontext.hash(password)

def validate_pass(plain_pass:str,hashed_pass:str) -> bool:
    return authconfig.passcontext.verify(plain_pass, hashed_pass)

def validate_user(formdata:OAuth2PasswordRequestForm,db:Session):
    user = crud.get_user_by_username(username=formdata.username, db=db)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect Username or Password')
    if not validate_pass(plain_pass=formdata.password,hashed_pass=user.password):
        raise HTTPException(status_code=401, detail= 'Incorrect Email or Password')

    return {"access_token": user.username, "token_type": "bearer"}
