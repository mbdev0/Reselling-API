from operations import crud
from auth import authconfig
from schemas import schemas
from configuration.dbconfig import interact_db

from typing import Union
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError


oauth2 = OAuth2PasswordBearer(tokenUrl='token')

def create_acess_token(data:dict, expiry_delta:Union[timedelta, None]= None):
    encode=data.copy()
    if expiry_delta:
        expiry = datetime.utcnow() + expiry_delta
    else:
        expiry = datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp':expiry})
    return jwt.encode(encode, key=authconfig.KEY, algorithm=authconfig.ALGORITHM)

def current_user(db: Session = Depends(interact_db) ,token:str = Depends(oauth2)):
    login_data_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials',
        headers={'WWW-Authenticate':'Bearer'}
        )
    try:
        data = jwt.decode(token=token, key=authconfig.KEY, algorithms=[authconfig.ALGORITHM])
        username:str = data.get('sub')
        if username is None:
            raise login_data_exception
        tokendata = schemas.TokenData(username=username)
    except JWTError:
        raise login_data_exception
    user = crud.get_user_by_username(username=tokendata.username, db=db)
    return user
    
def hash_pass(password:str) -> str:
    return authconfig.passcontext.hash(password)

def validate_pass(plain_pass:str,hashed_pass:str) -> bool:
    return authconfig.passcontext.verify(plain_pass, hashed_pass)

def validate_user(formdata:OAuth2PasswordRequestForm,db:Session):
    user = crud.get_user_by_username(username=formdata.username, db=db)
    if not user:
        return False
    if not validate_pass(plain_pass=formdata.password,hashed_pass=user.password):
        return False

    return user

def check_if_currUser(currUser, username):
    if currUser.username != username:
        print(currUser.username, username)
        raise HTTPException(
            status_code=401,
            detail='Unauthorized',
            headers={'WWW-Authenticate':'Bearer'}
        )
    else: return 