from fastapi import FastAPI, Depends
from core.config import setting
from database_files.engine import engine, Base
from routers.admin_route import admin_router
from routers.user_route import user_router
from routers.finance_route import finance_router
from fastapi.middleware.cors import CORSMiddleware

#read metadata, and instructing it to create tables using base schema.
Base.metadata.create_all(bind=engine)

#FastAPI Matadata.
app = FastAPI(  
    title = setting.TITLE, 
    description = setting.DESCRIPTION,
    contact= setting.CONTACT,
    version= setting.VERSION,
    openapi_tags= setting.TAGS
)

#CORS Middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

#registering the routers in our app.
app.include_router(admin_router, prefix="/admin", tags= ["Admin"])
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(finance_router, prefix="/finance", tags = ["Transactions"])
