from pymongo import ASCENDING
from config.db import db

students = db.get_collection("students")
students.create_index([("reg_no", ASCENDING)], unique=True)

def add_student(reg_no, name, dept, year, photo=None):
    students.update_one(
        {"reg_no": reg_no},
        {"$set": {
            "reg_no": reg_no,
            "name": name,
            "dept": dept,
            "year": year,
            "photo": photo
        }},
        upsert=True
    )

def get_all_students():
    return list(students.find().sort("reg_no", ASCENDING))

def get_student(reg_no):
    return students.find_one({"reg_no": reg_no})

def update_student(reg_no, name, dept, year, photo=None):
    update_data = {
        "name": name,
        "dept": dept,
        "year": year
    }

    # Add photo to update if provided
    if photo:
        update_data["photo"] = photo

    students.update_one(
        {"reg_no": reg_no},
        {"$set": update_data}
    )

def delete_student(reg_no):
    students.delete_one({"reg_no": reg_no})
    from models.marks import marks_collection
    marks_collection.delete_one({"reg_no": reg_no})
