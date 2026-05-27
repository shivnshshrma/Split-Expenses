from services.user_service import create_user
from core.security  import verify_password
from fastapi import HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import oauth2_scheme, get_current_user, create_access_session
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user_created


    

