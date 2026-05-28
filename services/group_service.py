from database.connection import supabase

def create_group(name: str, description: str, creator_by: str):
    group = supabase.table("groups").insert({"name": name, "description": description, "created_by": creator_by}).execute().data
    group_member = supabase.table("group_members").insert({"group_id": group[0]["id"], "user_id": creator_by, "role": "admin"}).execute().data
    return group

def get_user_groups(user_id: str):
    groups = supabase.table("group_members").select("group_id").eq("user_id", user_id).execute().data
    group_ids = [group["group_id"] for group in groups]
    if not group_ids:
        return []
    return supabase.table("groups").select("*").in_("id", group_ids).execute().data

def get_group_details(group_id: str):
    group_details = supabase.table("groups").select("*").eq("id", group_id).single().execute().data
    members = supabase.table("group_members").select("user_id, role").eq("group_id", group_id).execute().data 
    if not group_details:
        return []
    return {"group_details": group_details, "members": members} 

def add_member_to_group(user_id: str, group_id: str, role: str = "member"):
    return supabase.table("group_members").insert({"group_id": group_id, "user_id": user_id, "role": role}).execute().data

def remove_member_from_group(user_id: str, group_id: str):
    return supabase.table("group_members").delete().eq("group_id", group_id).eq("user_id", user_id).execute().data

def is_admin(group_id: str, user_id: str):
    member = supabase.table("group_members").select("role").eq("group_id", group_id).eq("user_id", user_id).single().execute().data
    return member and member["role"] == "admin"
    