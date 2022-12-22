from pydantic import BaseModel
# from datetime import datetime
from pydantic.schema import Optional


#--------------------------------- Admin management  ---------------------------------#
class AdminCreate(BaseModel):
    login: str 
    password: str 
    confirm_password: str 
    super_admin_key: str


class AdminResponse(BaseModel):
    login: str 

    class Config:
        orm_mode = True


#--------------------------------------------------------------------------------------#
#--------------------------------- User management  ---------------------------------#
class UserCreate(BaseModel):
    username: str 
    password: str 
    confirm_password: str 
    bank: str


class UserResponse(BaseModel):
    username: str 
    bank: str
    money: str

    class Config:
        orm_mode = True


class UserTransaction(BaseModel):
    amount: int
    token: str


class UserToUser(UserTransaction):
    to_user: str


class UserDepositResponse(BaseModel):
    amount: int
    deposited: bool
    new_balance: str

    class Config:
        orm_mode = True


class UserRetrieveResponse(BaseModel):
    amount: int
    retrieved: bool
    new_balance: str

    class Config:
        orm_mode = True


class UserToUserResponse(BaseModel):
    from_user: str
    to_user: str
    amount: int
    transferred: bool
    new_balance: str

    class Config:
        orm_mode = True


#--------------------------------------------------------------------------------------#
#--------------------------------- Bank management  ---------------------------------#
class BankCreate(BaseModel):
    acronym: str 
    name: str 


class BankResponse(BankCreate):
    money: str

    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Utils  ---------------------------------#

        
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: str

    class Config:
        orm_mode = True

        
class GetToken(BaseModel):
    token: str


class Token(BaseModel):
    token: str
    expire_time: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None
