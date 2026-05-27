from services.user_service import create_user, get_user_by_username
from core.security  import verify_password
from core.auth import get_current_user
from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import create_access_session
from schemas.user import User


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post('/signup')
async def signup(user: User):
    try:
        user_created = create_user(user)
        # create user and return 200 OK if successful, else return 400 Bad Request with error message
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user_created

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    print(f"User found: {user}")  # Debugging statement to check if user is retrieved correctly
    # check if user exists and password is correct, if not return 400 Bad Request with error message, else create and return access token   
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_session(data={"sub": user['username']})
    # return the access token and token type
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
    # login is successful, return the access token and token type

@router.get("/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    current_user.pop("password") # remove password from the user data before returning
    return current_user

