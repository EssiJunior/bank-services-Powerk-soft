from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, utils, oauth2
from typing import List 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
# from datetime import datetime

router = APIRouter(
    prefix="/user",
    tags=["User management"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_a_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.EntryException[1])
    else:
        bank = db.query(models.Bank).filter(models.Bank.acronym == user.bank).first()
        if bank == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.BankException[0])
    
        else:
            try:
                hashed_password = utils.hashed(user.password)
                user.password = hashed_password
                user = models.User(username=user.username, password=user.password, bank=user.bank)
                db.add(user)
                db.commit()
                db.refresh(user)
                    
                user.money = user.money  # CFA 
                
                return {"username": user.username, "bank": user.bank, "money": f"{user.money} CFA"}
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"The user << {user.username} >> already exists")


@router.post("/deposit", status_code=status.HTTP_200_OK, response_model=schemas.UserDepositResponse)
def deposit_in_account(entry: schemas.UserTransaction, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User Type: ", type(current_user))
    if isinstance(current_user, models.User): 
        bank = db.query(models.Bank).filter(models.Bank.acronym == current_user.bank).first()
        if bank == None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=utils.BankException[0])
        else:
            user = db.query(models.User).filter(models.User.username == current_user.username).first()
            if user == None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.UserException[0])
            else:
                new_amount = user.money + entry.amount
                user.update({"money": new_amount}, synchronize_session=False)
                bank.update({"money":bank.money + entry.amount}, synchronize_session=False)
                db.commit()
                return {"amount":entry.amount, "deposited":True, "new_balance":new_amount}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.UserException[1])

    
@router.post("/retrieve", status_code=status.HTTP_200_OK, response_model=schemas.UserRetrieveResponse)
def retrieve_from_account(entry: schemas.UserTransaction, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User Type: ", type(current_user))
    if isinstance(current_user, models.User): 
        user = db.query(models.User).filter(models.User.username == current_user.username).first()
        if user == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.UserException[0])
        else:
            new_amount = user.money - entry.amount
            if new_amount < 0:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, not enough money. (maximum: {user.first().money})")
            else:
                user.update({"money": new_amount}, synchronize_session=False)
                db.commit()
                return {"amount":entry.amount, "retrieved":True, "new_balance":new_amount}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.UserException[1])
    

@router.post("/transfer", status_code=status.HTTP_200_OK, response_model=schemas.UserToUserResponse)
def transfer_to_another(entry: schemas.UserToUser, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User Type: ", type(current_user))
    if isinstance(current_user, models.User): 
        from_user = db.query(models.User).filter(models.User.username == current_user.username).first()
        if from_user == None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=utils.UserException[0])
        else:
            to_user = db.query(models.User).filter(models.User.username == entry.to_user).first()
            if to_user == None:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=utils.UserException[0])
            else:
                if from_user.bank == to_user.bank:
                    from_user_new_amount = from_user.money - entry.amount
                    if from_user_new_amount < 0:
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, not enough money. (maximum: {from_user.money})")
                    else:
                        to_user_new_amount = to_user.money + entry.amount
                        from_user.update({"money": from_user_new_amount}, synchronize_session=False)
                        to_user.update({"money": to_user_new_amount}, synchronize_session=False)
                        
                        db.commit()
                        return {"amount":entry.amount, "transferred":True, "new_balance":from_user_new_amount, "to_user":to_user.username, "from_user":from_user.username}
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.UserException[2])
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.UserException[1])
    

@router.get("/all", response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def display_all_users(db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User Type: ", type(current_user))
    if isinstance(current_user, models.Admin): 
        users = db.query(models.User).all()
        
        for element in users:
            element.money = f"{element.money} CFA franc"
        return users

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])

    
@router.delete("", status_code=status.HTTP_200_OK)
def delete_a_user(username: str, db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User: ", type(current_user))
    if isinstance(current_user, models.Admin):
        user = db.query(models.User).filter(models.User.username == username)
        if user.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user << {username} >> does not exist ")
        else:
            user.delete(synchronize_session=False)
            db.commit()
            return {"message": f"User << {username} >> deleted."}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])

    
@router.delete("/all", status_code=status.HTTP_200_OK)
def delete_all_user(db: Session=Depends(get_db),
    current_user=Depends(oauth2.get_current_user)):
    print("Current User: ", type(current_user))
    if isinstance(current_user, models.Admin):
        user = db.query(models.User)
        user.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "All users deleted."}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=utils.AdminException[0])

