from fastapi import APIRouter, Depends, HTTPException, status
from core.auth import get_current_user
from services.group_service import create_group, get_user_groups, get_group_details, add_member_to_group, remove_member_from_group, is_admin
from schemas.group import GroupCreate, AddMember 

group_router = APIRouter(prefix="/groups", tags=["Groups"])

@group_router.post("/create")
def create_new_group(group: GroupCreate, current_user: dict = Depends(get_current_user)):
    return create_group(group.name, group.description, current_user["username"])

@group_router.get("/my-groups")
def list_user_groups(current_user: dict = Depends(get_current_user)):
    return get_user_groups(current_user["username"])

@group_router.get("/{group_id}")
def group_details(group_id: str, current_user: dict = Depends(get_current_user)):
    group_details = get_group_details(group_id)
    if not group_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group_details

@group_router.post("/{group_id}/add-member")
def add_member(group_id: str, member: AddMember, current_user: dict = Depends(get_current_user)):
    if not is_admin(group_id, current_user["username"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add members to this group")
    return add_member_to_group(member.username, group_id)   

@group_router.post("/{group_id}/remove-member")
def remove_member(group_id: str, member: AddMember, current_user: dict = Depends(get_current_user)):
    if not is_admin(group_id, current_user["username"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to remove members from this group")
    return remove_member_from_group(member.username, group_id)

