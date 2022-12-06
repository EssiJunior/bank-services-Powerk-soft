from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session
from . import schemas, database, models
from fastapi import Depends,status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print("--->Expire: ",expire)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")
    # type: ignore        
        if id is None:
            raise(credentials_exception)

        tokenData = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    return tokenData

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials"
    , headers= {"WWW-Authenticate":"Bearer"})
    tokenD = verify_access_token(token, credentials_exception)
    admin = db.query(models.Admin).filter(models.Admin.login == tokenD.id).first()
    if admin == None:
        user = db.query(models.User).filter(models.User.username == tokenD.id).first()
        if user == None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Not a user type. ")
        else:
            return user
    else:
        return admin

