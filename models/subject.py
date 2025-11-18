from pymongo import ASCENDING
from config.db import db

subjects = db.get_collection("subjects")

subjects.create_index([("dept", ASCENDING), ("code", ASCENDING)], unique=True)

SUBJECT_SETS = {
    "CSE": [
        {"code": "21CS7601", "name": "Cloud Computing"},
        {"code": "21CS7602", "name": "Cryptography and Network Security"},
        {"code": "21CS7708", "name": "5G Communication"},
        {"code": "21CS7S01", "name": "Cloud Laboratory"},
    ],
    "CIVIL": [
        {"code": "21HS6101", "name": "Total Quality"},
        {"code": "21CE7701", "name": "Estimated and Cost Analysis"},
        {"code": "21EE7801", "name": "Electrical Equipment Safety"},
        {"code": "21ME7807", "name": "Safety Measures for Engineers"},
    ],
    "ECE": [
        {"code": "21HS6101", "name": "Total Quality Management"},
        {"code": "21EE7601", "name": "Renewable Energy Systems"},
        {"code": "21ME7801", "name": "Industrial Economics and Foreign Trade"},
        {"code": "21ME7807", "name": "Safety Measures for Engineers"},
    ],
    "IT": [
        {"code": "21HS6101", "name": "Total Quality Management"},
        {"code": "21IT7601", "name": "Machine Learning"},
        {"code": "21IT7709", "name": "UI/UX Design"},
        {"code": "21IT7S04", "name": "Business Intelligence and Analytics"},
    ],
}

def seed_subjects():
    for dept, subs in SUBJECT_SETS.items():
        for s in subs:
            subjects.update_one(
                {"dept": dept, "code": s["code"]},
                {"$set": {"dept": dept, "code": s["code"], "name": s["name"]}},
                upsert=True
            )

def get_subjects_by_dept(dept):
    return list(subjects.find({"dept": dept}).sort("code", ASCENDING))

def all_subjects_grouped():
    result = {}
    for d in subjects.distinct("dept"):
        result[d] = list(subjects.find({"dept": d}).sort("code", ASCENDING))
    return result
