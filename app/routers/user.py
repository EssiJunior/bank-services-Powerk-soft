from fastapi import status, Depends , HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, config, utils, oauth2
from typing import List 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/user",
    tags=["User management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_a_user(user: schemas.UserCreate, db: Session = Depends(get_db) ): 
    if user.password != user.confirm_password:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Le champs 'password' et 'confirm_password' sont differents")
    else:
        bank = db.query(models.Bank).filter(models.Bank.acronym == user.bank).first()
        print(bank)
        if bank == None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The specified acronym does not identify a bank in our system. " )
    
        else:
            try:
                hashed_password = utils.hashed(user.password)
                user.password = hashed_password
                user = models.User(username=user.username, password=user.password, bank=user.bank)
                db.add(user)
                db.commit()
                db.refresh(user)
                    
                return user
            except IntegrityError:
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"The username << {user.username} >> already exist")
                
                


@router.get("/all", response_model= List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def display_all_users(db: Session = Depends(get_db)):  
    users = db.query(models.User).all()
    return users

@router.delete("", status_code=status.HTTP_200_OK)
def delete_a_user(username: str, db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Admin):
        user = db.query(models.User).filter(models.User.username == username)
        if user.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"The user << {username} >> does not exist ")
        else:
            user.delete(synchronize_session = False)
            db.commit()
            return {"message": f"User << {username} >> deleted."}

    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, admin functionality.")
    
@router.delete("/all", status_code=status.HTTP_200_OK)
def delete_all_user(db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Admin):
        user = db.query(models.User)
        user.delete(synchronize_session = False)
        db.commit()
        
        return {"message": "All users deleted."}

    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, admin functionality.")


