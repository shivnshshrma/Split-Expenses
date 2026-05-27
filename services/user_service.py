from database.connection import supabase
from core.security import hash_password

def create_user(user):
    hashed_password = hash_password(user.password) # take the password and hash it before storing in db
    user_data = {
        "username": user.username,  
        "name": user.name,           #create a user data dict to insert into db
        "email": user.email,
        "password": hashed_password,
        "phone_number": user.phone_number
    }
    if_exists_user = get_user_by_username(user.username) # check if user already exists in db, if yes raise exception, else create user
    if_exists_email = supabase.table('users').select("*").eq("email", user.email).execute().data
    if if_exists_user:
        raise Exception("Username already exists")
    elif if_exists_email:
        raise Exception("Email already exists")
    else:
        supabase.table('users').insert(user_data).execute()
        return {"message": "200 OK"}
    

def get_user_by_username(username: str):
    user = supabase.table('users').select("*").eq("username", username).execute()
    if user.data:
        return user.data[0]
    return None
