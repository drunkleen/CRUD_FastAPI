from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from app import models
from app.database import Session, get_db
from app.utility import hash_password
from app.schema import users

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[users.GetUser])
async def get_all_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=users.GetUser)
async def create_user(n_user: users.UserCreate, datab: Session = Depends(get_db)):
    # hashing password:
    n_user.password = hash_password(n_user.password)
    # create the user
    new_user = models.User(**n_user.dict())
    datab.add(new_user)
    datab.commit()
    datab.refresh(new_user)

    return new_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=users.GetUser)
async def get_user(user_id: int, datab: Session = Depends(get_db)):
    user = datab.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with {user_id} doesn't exist.")

    return user
