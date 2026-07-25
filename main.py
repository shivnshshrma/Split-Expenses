from fastapi import FastAPI
from api.endpoints.auth import router
from api.endpoints.user import user_router
from api.endpoints.groups import group_router
from database.connection import engine, Base
import database.models

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(router)
app.include_router(user_router)
app.include_router(group_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Split Expenses API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
