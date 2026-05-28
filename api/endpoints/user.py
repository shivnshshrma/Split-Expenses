from core.auth import get_current_user
from fastapi import APIRouter, Depends
from schemas.user import UserUpdate
from services.user_service import update_user_info, search_users_by_query


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@user_router.put("/me")
async def update_user_me(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    """ Update the current user's information. This endpoint is protected and requires authentication.
    The user can update their information such as email, full name, etc. The password cannot be updated through this endpoint.
    """
    update_user_info(current_user["username"], user_update) # call the update_user_info function from user_service to update the user's information in the database
    return {"message": "User information updated successfully"}

@user_router.get("/search")
async def search_users(query: str, current_user: dict = Depends(get_current_user)):
    """ Search for users by username or email. This endpoint is protected and requires authentication.
    The search query can be a partial match for the username or email. The results will include users that match the query.
    """
    users = search_users_by_query(query) # call the search_users_by_query function from user_service to search for users in the database based on the query
    return {"users": users}

