from configuration.dbconfig import interact_db
from configuration.limiter import *
from schemas import schemas
from auth import auth
from operations import crud

from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request


router = APIRouter()

@router.post("/user", response_model=schemas.User, tags=['User'])
@limiter.limit("10/minute")
def create_user(
    request: Request,
    user: schemas.UserCreation, 
    db: Session = Depends(interact_db)):
    return crud.create_user(db=db,user=user)

@router.get("/users", response_model=List[schemas.User], tags=['User'])
@limiter.limit("30/minute")
def get_all_users(
    request:Request,
    db:Session = Depends(interact_db),
    currUser = Depends(auth.current_user)):
    if currUser.superuser:
        return crud.get_all_users(db=db)
    else:
        raise HTTPException(status_code=401, detail='Unauthorized',headers={'WWW-Authenticate':'Bearer'})

@router.get('/{username}', response_model = schemas.User, tags=['User'])
@limiter.limit("30/minute")
def get_user_by_id(
    request:Request,
    username:str,
    currUser: schemas.User = Depends(auth.current_user) ,
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        resp = crud.get_user_by_username(username=username, db=db)
        if resp is None:
            raise HTTPException(status_code=404, detail=f"User not found with username: {username}")
        return resp
    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.get_user_by_username(username=username, db=db)

@router.patch('/{username}', response_model=schemas.User, tags=['User'])
@limiter.limit("30/minute")
def update_user(
    request: Request,
    username: str, 
    user: schemas.UserCreation, 
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.update_user(username=username, user=user, db=db)
    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.update_user(username=username, user=user, db=db)

@router.delete('/{username}',response_model=dict, tags=['User'])
@limiter.limit("10/minute")
def delete_user_by_username(
    request:Request,
    username:str,
    currUser:schemas.User = Depends(auth.current_user),
    db: Session = Depends(interact_db)):

    if currUser.superuser:
        print(currUser.superuser)
        return crud.delete_user_by_username(username=username, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.delete_user_by_username(username=username, db=db)

@router.get('/{username}/storage', response_model = schemas.Storage, tags=['Storage'])
@limiter.limit("60/minute")
def get_storage_by_username(
    request:Request,
    username:str,
    currUser:schemas.User = Depends(auth.current_user),
    db:Session = Depends(interact_db)):

    if currUser.superuser:
        return crud.get_user_storage(username=username, db=db)

    auth.check_if_currUser(currUser=currUser, username=username)
    return crud.get_user_storage(username=username, db=db)
