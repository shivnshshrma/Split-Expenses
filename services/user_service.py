from database.connection import SessionLocal
from database.models import User
from core.security import hash_password

def create_user(user):
    hashed_password = hash_password(user.password) # hash password before storing in db
    
    with SessionLocal() as db:
        if_exists_user = db.query(User).filter(User.username == user.username).first()
        if_exists_email = db.query(User).filter(User.email == user.email).first()
        
        if if_exists_user:
            raise Exception("Username already exists")
        elif if_exists_email:
            raise Exception("Email already exists")
        
        db_user = User(
            username=user.username,
            name=user.name,
            email=user.email,
            password=hashed_password,
            phone_number=user.phone_number
        )
        db.add(db_user)
        db.commit()
        return {"message": "User created successfully"}

def get_user_by_username(username: str):
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == username).first()
        if user:
            return {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "phone_number": user.phone_number
            }
        return None

def update_user_info(username: str, user_update):
    update_user_data = {k: v for k, v in user_update.dict().items() if v is not None} # dict of fields to update
    if not update_user_data:
        raise Exception("No valid fields to update")
        
    with SessionLocal() as db:
        db_user = db.query(User).filter(User.username == username).first()
        if not db_user:
            raise Exception("User not found")
            
        for key, value in update_user_data.items():
            setattr(db_user, key, value)
            
        db.commit()
        return {"message": "200 OK"}

def search_users_by_query(query: str):
    with SessionLocal() as db:
        users = db.query(User).filter(
            (User.username.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
        ).all()
        return [{"username": u.username, "email": u.email} for u in users]
