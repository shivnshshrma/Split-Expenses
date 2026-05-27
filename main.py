from fastapi import FastAPI, Depends, HTTPException, status
import os
from core.auth import oauth2_scheme, get_current_user, create_access_session
from api.endpoints.auth import router


app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Split Expenses API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

