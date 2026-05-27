from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import os
import supabase
from supabase import create_client, Client
from auth.authentication import oauth2_scheme, get_current_user, create_access_session
from models.User import User



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)    

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)




@app.get('/')
async def root():
    return {"message": "Welcome to Split Expenses API"}

@app.get('/health')
def health_check():
    return {"status": "ok"}

@app.post('/signup')
async def signup(user: User):
    create_user(user)
    return {"message": "User created successfully"}


@app.get('/login')
async def login():
    pass


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = supabase.table('users').select("*").eq("username", form_data.username).execute().data
    user = user[0] if user else None
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_session(data={"sub":user.username})
    return {"access_token":access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}

def create_user(user: User):
    # check existing user by email or username
    exists = supabase.table("users").select("id").or_(f"email.eq.{user.email},username.eq.{user.username}").execute()
    if exists.data:
        raise HTTPException(status_code=409, detail="User with that email or username already exists")

    # insert user
    hashed_password = hash_password(user.password)
    res = supabase.table("users").insert({
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "phone": user.phone
    }).execute()

    if getattr(res, "error", None):
        raise HTTPException(status_code=500, detail=str(res.error))

    created = res.data[0] if res.data else None
    return {"message": "User created successfully", "user": created}
    

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    """ Hash the password using bcrypt """
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verify the password against the hashed password """
    return pwd_context.verify(plain_password, hashed_password)


