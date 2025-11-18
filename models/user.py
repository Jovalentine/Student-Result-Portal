from pymongo import ASCENDING
from werkzeug.security import generate_password_hash, check_password_hash
from config.db import db

users = db.get_collection("users")
users.create_index([("username", ASCENDING)], unique=True)

# Create admin account initially
def create_admin(username, password):
    users.update_one(
        {"username": username},
        {"$set": {"username": username, "password": generate_password_hash(password), "role": "admin"}},
        upsert=True
    )

def create_student_login(reg_no, password):
    users.update_one(
        {"username": reg_no},
        {"$set": {"username": reg_no, "password": generate_password_hash(password), "role": "student"}},
        upsert=True
    )

def verify_user(username, password):
    user = users.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        return user
    return None

def update_student_password(username, new_password):
    users_collection.update_one(
        {"username": username},
        {"$set": {"password": generate_password_hash(new_password)}}
    )
