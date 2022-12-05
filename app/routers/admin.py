from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, config, utils, oauth2
from typing import List 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/admin",
    tags=["Admin management"]
)


@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
def create_an_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)):
    if current_user.login == "Powerk-soft":  
        print("Current User: ",current_user.login)
        if admin.password != admin.confirm_password:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Le champs 'password' et 'confirm_password' sont differents")
        else:
            if admin.super_admin_key != config.settings.super_admin_key:
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Cle du super admin incorrect ( Contact: +237 690743737 )")
            
            else:
                try:
                    hashed_password = utils.hashed(admin.password)
                    admin.password = hashed_password
                    admin = models.Admin(login=admin.login, password=admin.password)
                    db.add(admin)
                    db.commit()
                    db.refresh(admin)
                        
                    return {"login": admin.login, "password":admin.password,
                                "created_ant": datetime.now()}
                except IntegrityError:
                    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"le login << {admin.login} >> existe deja")
                
                

    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, super admin functionality.")

@router.get("/all", response_model= List[schemas.AdminResponse], status_code=status.HTTP_200_OK)
def display_all_admins(db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)):
    print("Current User Type: ",type(current_user))
    if isinstance(current_user, models.Admin):    
        admins = db.query(models.Admin).all()
        return admins

    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, admin functionality.")
    
@router.delete("", status_code=status.HTTP_200_OK)
def delete_an_admin(login: str,super_admin_key: str, db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)):
    if current_user.login == "Powerk-soft":  
        print("Current User: ",current_user.login) 
        if super_admin_key != config.settings.super_admin_key:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Cle du super admin incorrect ( Contact: +237 690743737 )")
        
        else:
            admin = db.query(models.Admin).filter(models.Admin.login == login)
            if admin.first() == None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La admin << {login} >> n'existe pas ")
            else:
                admin.delete(synchronize_session = False)
                db.commit()
                return {"message": f"l'admin << {login} >> est supprimé avec succes."}

    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, admin functionality.")
    
@router.delete("/all", status_code=status.HTTP_200_OK)
def delete_all_admin(super_admin_key:str, db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)):
    if current_user.login == "Powerk-soft":  
        print("Current User: ",current_user.login)
        if super_admin_key != config.settings.super_admin_key:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Cle du super admin incorrect ( Contact: +237 690743737 )")
        else:
            admin = db.query(models.Admin)
            admin.delete(synchronize_session = False)
            db.commit()
            
            return {"message": "Suppression de toutes les admins avec succes."}

    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, admin functionality.")
