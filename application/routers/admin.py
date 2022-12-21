from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, config, utils, oauth2
from typing import List 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Admin management"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
def create_an_admin(admin: schemas.AdminCreate, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    if current_user.login == "Powerk-soft": 
        print("Current User: ", current_user.login)
        if admin.password != admin.confirm_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.EntryException[1])
        else:
            if admin.super_admin_key != config.settings.super_admin_key:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.SuperAdminException[0])
            
            else:
                try:
                    hashed_password = utils.hashed(admin.password)
                    admin.password = hashed_password
                    admin = models.Admin(login=admin.login, password=admin.password)
                    db.add(admin)
                    db.commit()
                    db.refresh(admin)
                        
                    return {"login": admin.login, "password":admin.password}
                
                except IntegrityError:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login << {admin.login} >> already exists")

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.SuperAdminException[1])


@router.get("/all", response_model=List[schemas.AdminResponse], status_code=status.HTTP_200_OK)
def display_all_admins(db: Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    if current_user.login == "Powerk-soft": 
        admins = db.query(models.Admin).all()
        return admins

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.SuperAdminException[1])

    
@router.delete("", status_code=status.HTTP_200_OK)
def delete_an_admin(login: str, super_admin_key: str, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    if current_user.login == "Powerk-soft": 
        print("Current User: ", current_user.login) 
        if super_admin_key != config.settings.super_admin_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.SuperAdminException[0])
        
        else:
            admin = db.query(models.Admin).filter(models.Admin.login == login)
            if admin.first() == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The admin << {login} >> doesn't exist ")
            else:
                admin.delete(synchronize_session=False)
                db.commit()
                return {"message": f"The admin << {login} >> is successfully deleted."}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.SuperAdminException[1])

    
@router.delete("/all", status_code=status.HTTP_200_OK)
def delete_all_admin(super_admin_key:str, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    if current_user.login == "Powerk-soft": 
        print("Current User: ", current_user.login)
        if super_admin_key != config.settings.super_admin_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.SuperAdminException[0])
        else:
            admin = db.query(models.Admin).filter(models.Admin.login != current_user.login)
            admin.delete(synchronize_session=False)
            db.commit()
            
            return {"message": "All admins deleted successfully."}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.SuperAdminException[1])
