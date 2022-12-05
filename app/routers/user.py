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

@router.post("/login", response_model=schemas.LoginResponse)
def login(user_log: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_log.username).first()
    user_type: str
    
    if not user:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=utils.no_account())
    else:    
        if not utils.verified(user_log.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=utils.incorrect_pass())
        access_token = oauth2.create_access_token(data= {"user_id": user.login})
        user_type = "user"
        return {"access_token": access_token, "token_type": "Bearer", "user": user_type}

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_an_user(user: schemas.userCreate, db: Session = Depends(get_db) ): 
    if user.password != user.confirm_password:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Le champs 'password' et 'confirm_password' sont differents")
    else:
        if user.super_user_key != config.settings.super_user_key:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Cle du super user incorrect ( Contact: +237 690743737 )")
        
        else:
            try:
                hashed_password = utils.hashed(user.password)
                user.password = hashed_password
                user = models.User(login=user.login, password=user.password)
                db.add(user)
                db.commit()
                db.refresh(user)
                    
                return {"login": user.login, "password":user.password,
                            "created_ant": datetime.now()}
            except IntegrityError:
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"le login << {user.login} >> existe deja")
                
                


@router.get("/all", response_model= List[schemas.userResponse], status_code=status.HTTP_200_OK)
def display_all_users(db: Session = Depends(get_db)):  
    users = db.query(models.User).all()
    return users

@router.delete("", status_code=status.HTTP_200_OK)
def delete_an_user(login: str,super_user_key: str, db: Session = Depends(get_db)): 
    if super_user_key != config.settings.super_user_key:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Cle du super user incorrect ( Contact: +237 690743737 )")
    
    else:
        user = db.query(models.User).filter(models.User.login == login)
        if user.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La user << {login} >> n'existe pas ")
        else:
            user.delete(synchronize_session = False)
            db.commit()
            return {"message": f"l'user << {login} >> est supprimé avec succes."}
    
@router.delete("/all", status_code=status.HTTP_200_OK)
def delete_all_user(super_user_key:str, db: Session = Depends(get_db)): 
    if super_user_key != config.settings.super_user_key:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Cle du super user incorrect ( Contact: +237 690743737 )")
    else:
        user = db.query(models.User)
        user.delete(synchronize_session = False)
        db.commit()
        
        return {"message": "Suppression de toutes les users avec succes."}

