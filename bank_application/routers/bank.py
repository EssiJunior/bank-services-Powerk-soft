from fastapi import APIRouter, status, Depends, HTTPException
import schemas, models, oauth2, utils
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router = APIRouter(
    prefix="/bank",
    tags=["Bank management"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.BankResponse)
def create_a_bank(bank: schemas.BankCreate, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User: ", type(current_user))
    if isinstance(current_user, models.Admin):
        bank = models.Bank(acronym=bank.acronym, name=bank.name)
        db.add(bank)
        db.commit()
        db.refresh(bank)
        
        return {"acronym":bank.acronym, "name":bank.name, "money":f"{bank.money} CFA"}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])

    
@router.get("", status_code=status.HTTP_200_OK, response_model=schemas.BankResponse)
def display_a_bank(acronym:str, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User: ", type(current_user))
    if isinstance(current_user, models.Admin):
        bank = db.query(models.Bank).filter(models.Bank.acronym == acronym).first()
        if bank == None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=utils.BankException[0])
        
        bank.money = f"{bank.money} CFA franc"
        return bank

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])

    
@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[schemas.BankResponse])
def display_all_banks(db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User: ", type(current_user))
    if isinstance(current_user, models.Admin):
        bank = db.query(models.Bank).all()
        
        for element in bank:
            element.money = f"{element.money} CFA franc"
        return bank

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])

    
@router.put("", status_code=status.HTTP_200_OK, response_model=schemas.BankResponse)
def update_a_bank(acronym: str, bank: schemas.BankCreate, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User: ", type(current_user))
    if isinstance(current_user, models.Admin):
        request = db.query(models.Bank).filter(models.Bank.acronym == acronym).first()
        if request == None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=utils.BankException[0])
        request.update(bank.dict(), synchronize_session=False)
        db.commit()
        
        return {"acronym":request.acronym, "name":request.name, "money":f"{request.money} CFA"}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])

    
@router.delete("", status_code=status.HTTP_200_OK)
def delete_a_bank(acronym: str, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User: ", type(current_user))
    if isinstance(current_user, models.Admin):
        request = db.query(models.Bank).filter(models.Bank.acronym == acronym)
        if request == None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=utils.BankException[0])
        request.delete(synchronize_session=False)
        db.commit()
        return {"message":f"Successfully deleted {acronym} bank"}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])

    
@router.delete("/all", status_code=status.HTTP_200_OK)
def delete_all_bank(db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User: ", type(current_user))
    if isinstance(current_user, models.Admin):
        request = db.query(models.Bank)
        request.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully deleted all the banks"}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])
    
