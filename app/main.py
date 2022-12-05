from fastapi import FastAPI #, Depends , HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
from .database import engine 
from . import models #, schemas, utils


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
# app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Hello world"}

