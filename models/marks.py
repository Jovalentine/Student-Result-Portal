from config.db import db

marks_collection = db.get_collection("marks")

def save_marks(reg_no, marks_dict):
    # total marks obtained
    total_obtained = sum(marks_dict.values())

    # each subject out of 100
    total_max = len(marks_dict) * 100

    # percentage calculation
    percentage = (total_obtained / total_max) * 100

    # pass / fail: 40% rule
    result = "PASS" if percentage >= 40 else "FAIL"

    marks_collection.update_one(
        {"reg_no": reg_no},
        {
            "$set": {
                "reg_no": reg_no,
                "marks": marks_dict,
                "total": total_obtained,
                "percentage": round(percentage, 2),
                "result": result
            }
        },
        upsert=True
    )

def get_marks(reg_no):
    return marks_collection.find_one({"reg_no": reg_no}) or {
        "marks": {},
        "total": 0,
        "percentage": 0,
        "result": "FAIL"
    }
