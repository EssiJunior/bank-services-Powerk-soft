from fastapi import FastAPI ,status, Depends , HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models , schemas, utils, oauth2
from .routers import admin, bank, user

models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

# --------------------------- Swagger UI customization --------------------------- #
def custom_openapi():      
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="bank-services-Powerk-soft",
        version="0.1",
        description="Basic APIs of bank system",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
# ---------------------------++++++++++++++++++++++++++++--------------------------- #

app.openapi = custom_openapi
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"] 
)

# --------------------------- routers --------------------------- #
app.include_router(admin.router)
app.include_router(bank.router)
app.include_router(user.router)

@app.get("/")
def root():
    print(utils.hashed("Powerk-soft"))
    return {"message": "Hello world"}


@app.post("/login", response_model=schemas.LoginResponse)
def login(user_log: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_log.username).first()
    user_type: str
    
    if not user:
        admin = db.query(models.Admin).filter(models.Admin.login == user_log.username).first()
        if not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=utils.no_account())
        else:
            if not utils.verified(user_log.password, admin.password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=utils.incorrect_pass())
            access_token = oauth2.create_access_token(data= {"user_id": admin.login})
            user_type = "admin"
            return {"access_token": access_token, "token_type": "Bearer", "user": user_type}
            
    else:    
        if not utils.verified(user_log.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=utils.incorrect_pass())
        access_token = oauth2.create_access_token(data= {"user_id": user.username})
        user_type = "user"
        return {"access_token": access_token, "token_type": "Bearer", "user": user_type}


@app.get("/logout", response_model=schemas.LoginResponse)
def logout(db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Admin):
        ...
        #TODO
        
    elif isinstance(current_user, models.User):
        ...
        #TODO
    
    else:
        ...
        #TODO