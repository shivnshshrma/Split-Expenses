from database.connection import supabase
from core.security import hash_password

def create_user(user):

    hashed_password = hash_password(user.password) # take the password and hash it before storing in db
    user_data = {
        "username": user.username,          #create a user data dict to insert into db
        "email": user.email,
        "password": hashed_password,
        "full_name": user.name,
        "phone_number": user.phone_number
    }
    if_exists_user = supabase.table('users').select("*").eq("username", user.username).execute().data
    if_exists_email = supabase.table('users').select("*").eq("email", user.email).execute().data
    if if_exists_user or if_exists_email:
        raise Exception("User already exists")
    else:
        supabase.table('users').insert(user_data).execute()
        return {"message": "200 OK"}
    
