from database.connection import SessionLocal
from database.models import Group, GroupMember

def create_group(name: str, description: str, creator_by: str):
    with SessionLocal() as db:
        db_group = Group(name=name, description=description, created_by=creator_by)
        db.add(db_group)
        db.flush() # generates the default UUID id
        
        group_member = GroupMember(group_id=db_group.id, user_id=creator_by, role="admin")
        db.add(group_member)
        db.commit()
        
        return [{"id": db_group.id, "name": db_group.name, "description": db_group.description, "created_by": db_group.created_by}]

def get_user_groups(user_id: str):
    with SessionLocal() as db:
        groups = db.query(Group).join(GroupMember, Group.id == GroupMember.group_id).filter(GroupMember.user_id == user_id).all()
        return [{"id": g.id, "name": g.name, "description": g.description, "created_by": g.created_by} for g in groups]

def get_group_details(group_id: str):
    with SessionLocal() as db:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            return None
            
        members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
        
        group_details = {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "created_by": group.created_by
        }
        members_data = [{"user_id": m.user_id, "role": m.role} for m in members]
        return {"group_details": group_details, "members": members_data} 

def add_member_to_group(user_id: str, group_id: str, role: str = "member"):
    with SessionLocal() as db:
        group_member = GroupMember(group_id=group_id, user_id=user_id, role=role)
        db.add(group_member)
        db.commit()
        return [{"group_id": group_id, "user_id": user_id, "role": role}]

def remove_member_from_group(user_id: str, group_id: str):
    with SessionLocal() as db:
        db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).delete()
        db.commit()
        return [{"group_id": group_id, "user_id": user_id}]

def is_admin(group_id: str, user_id: str):
    with SessionLocal() as db:
        member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        return member is not None and member.role == "admin"