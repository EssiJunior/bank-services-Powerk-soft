from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/bank",
    tags = ["Bank management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model = schemas.BankResponse)
def create_a_bank(bank: schemas.BankCreate, db: Session = Depends(get_db)):
    bank = models.Bank(acronym=bank.acronym, name=bank.name)
    db.add(bank)
    db.commit()
    db.refresh(bank)
    return bank

@router.get("", status_code = status.HTTP_200_OK, response_model = schemas.BankResponse)
def display_a_bank(acronym:str, db: Session = Depends(get_db)):
    request = db.query(models.Bank).filter(models.Bank.acronym == acronym).first()
    if request == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The specified acronym does not identify a bank in our system. " )
    
    return request

@router.get("/all", status_code = status.HTTP_200_OK, response_model = List[schemas.BankResponse])
def display_all_banks(db: Session = Depends(get_db)):
    request = db.query(models.Bank).all()
    return request
    
@router.put("", status_code = status.HTTP_200_OK, response_model = schemas.BankResponse)
def update_a_bank(acronym: str, bank: schemas.BankCreate,db: Session = Depends(get_db)):
    request = db.query(models.Bank).filter(models.Bank.acronym == acronym)
    if request == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The specified acronym does not identify a bank in our system." )
    request.update(bank.dict(), synchronize_session= False)
    db.commit()
    return bank

@router.delete("", status_code = status.HTTP_200_OK)
def delete_a_bank(acronym: str,db: Session = Depends(get_db)):
    request = db.query(models.Bank).filter(models.Bank.acronym == acronym)
    if request == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The specified acronym does not identify a bank in our system." )
    request.delete(synchronize_session=False)
    db.commit()
    return {"message":f"Successfully deleted {acronym} bank"}

@router.delete("/all", status_code = status.HTTP_200_OK)
def delete_all_bank(db: Session = Depends(get_db)):
    request = db.query(models.Bank)
    request.delete(synchronize_session=False)
    db.commit()
    return {"message":"Successfully deleted all the banks"}