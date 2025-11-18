from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from models.user import create_student_login, update_student_password
from models.student import add_student, get_all_students, get_student, update_student, delete_student
from models.subject import get_subjects_by_dept, all_subjects_grouped
from models.marks import save_marks, get_marks
from werkzeug.utils import secure_filename

import os, io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

student_bp = Blueprint("students", __name__)

# ------------------ Auth Helpers ------------------
def is_admin():
    return session.get("role") == "admin"

def is_student(reg_no):
    return session.get("role") == "student" and session.get("user") == reg_no

UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------ Admin Home ------------------
@student_bp.route("/admin")
def admin_home():
    if not is_admin():
        return redirect(url_for("auth.login"))
    return render_template("admin_home.html")

# ------------------ Register Student ------------------
@student_bp.route("/admin/student/register", methods=["GET", "POST"])
def admin_register_student():
    if not is_admin():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        reg_no = request.form["reg_no"].strip()
        name = request.form["name"].strip()
        dept = request.form["dept"]
        year = request.form["year"]
        password = request.form["password"].strip()

        photo_file = request.files.get("photo")
        photo_filename = None
        if photo_file and allowed_file(photo_file.filename):
            photo_filename = secure_filename(photo_file.filename)
            photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
            photo_file.save(photo_path)

        add_student(reg_no, name, dept, year, photo_filename)
        create_student_login(reg_no, password)

        flash("✅ Student registered successfully.", "success")
        return redirect(url_for("students.admin_register_student"))

    return render_template("student_register.html")

# ------------------ Admin Student List ------------------
@student_bp.route("/admin/students")
def admin_students():
    if not is_admin():
        return redirect(url_for("auth.login"))
    students = get_all_students()
    return render_template("students_list.html", students=students)

# ------------------ Subject List ------------------
@student_bp.route("/admin/subjects")
def admin_subjects():
    if not is_admin():
        return redirect(url_for("auth.login"))
    grouped = all_subjects_grouped()
    return render_template("subjects.html", grouped=grouped)

# ------------------ Enter Marks ------------------
@student_bp.route("/admin/result", methods=["GET", "POST"])
def admin_result_entry():
    if not is_admin():
        return redirect(url_for("auth.login"))

    students = get_all_students()
    selected_student = None
    subjects = None

    reg_no = request.args.get("reg_no")
    if reg_no:
        selected_student = get_student(reg_no)
        if selected_student:
            subjects = get_subjects_by_dept(selected_student["dept"])

    if request.method == "POST":
        reg_no = request.form.get("reg_no")
        selected_student = get_student(reg_no)
        subjects = get_subjects_by_dept(selected_student["dept"])
        marks_dict = {s["code"]: int(request.form.get(s["code"], 0)) for s in subjects}
        save_marks(reg_no, marks_dict)
        flash("✅ Marks Saved", "success")
        return redirect(url_for("students.admin_result_entry", reg_no=reg_no))

    return render_template("result_entry.html", students=students, student=selected_student, subjects=subjects)

# ----------------------------------------------------------
# ✅ Student Dashboard (Before viewing result)
# ----------------------------------------------------------
@student_bp.route("/student/<reg_no>")
def student_home(reg_no):
    if not is_student(reg_no):
        return redirect(url_for("auth.login"))
    profile = get_student(reg_no)
    return render_template("student_home.html", profile=profile)

# ----------------------------------------------------------
# ✅ Student Result View (THIS ROUTE WAS MISSING)
# ----------------------------------------------------------
@student_bp.route("/student/<reg_no>/result")
def student_result(reg_no):
    if not is_student(reg_no):
        return redirect(url_for("auth.login"))
    profile = get_student(reg_no)
    subjects = get_subjects_by_dept(profile["dept"])
    result = get_marks(reg_no)

    if not result:
        flash("⚠️ No result uploaded yet.", "warning")
        return redirect(url_for("students.student_home", reg_no=reg_no))

    return render_template("student_view.html", profile=profile, subjects=subjects, result=result)

# ----------------------------------------------------------
# ✅ Download Result PDF
# ----------------------------------------------------------
@student_bp.route("/student/<reg_no>/download")
def download_result(reg_no):
    if not is_student(reg_no):
        return redirect(url_for("auth.login"))

    student = get_student(reg_no)
    result = get_marks(reg_no)
    subjects = get_subjects_by_dept(student["dept"])

    if not result:
        flash("⚠️ No result uploaded yet.", "warning")
        return redirect(url_for("students.student_result", reg_no=reg_no))

    COLLEGE_NAME = "𝗦𝗼𝗼𝘆𝗮𝗮 𝗖𝗼𝗹𝗹𝗲𝗴𝗲 𝗼𝗳 𝗧𝗲𝗰𝗵𝗻𝗼𝗹𝗼𝗴𝘆"  # C3
    PASS_THRESHOLD = 50

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 45
    y = height - 60

    # Title
    p.setFont("Helvetica-Bold", 22)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, y, COLLEGE_NAME)
    y -= 30

    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, y, "STUDENT RESULT REPORT")
    y -= 40

    # Student Info Left
    p.setFont("Helvetica", 12)
    p.drawString(margin, y, f"Name      : {student.get('name', '-')}")
    y -= 18
    p.drawString(margin, y, f"Reg No    : {student.get('reg_no', '-')}")
    y -= 18
    p.drawString(margin, y, f"Department: {student.get('dept', '-')}")
    y -= 18
    p.drawString(margin, y, f"Year      : {student.get('year', '-')}")
    
    # Student Photo Right (S2: Clean Square)
    photo_name = student.get("photo")
    photo_size = 95
    photo_x = width - margin - photo_size
    photo_y = height - 175

    try:
        if photo_name:
            img_path = os.path.join("static", "uploads", photo_name)
            if os.path.exists(img_path):
                p.drawImage(ImageReader(img_path), photo_x, photo_y, width=photo_size, height=photo_size, mask=None)
    except:
        pass

    y -= 35
    p.line(margin, y, width - margin, y)
    y -= 28

    # Marks Summary
    total = result.get("total", 0)
    percentage = result.get("percentage", 0)
    status = "PASS ✅" if percentage >= PASS_THRESHOLD else "FAIL ❌"

    p.setFont("Helvetica-Bold", 12)
    p.drawString(margin, y, f"Total Marks: {total}")
    p.drawString(margin + 180, y, f"Percentage: {percentage}%")
    p.drawString(margin + 350, y, f"Status: {status}")
    y -= 30

    # Table Header
    p.setFont("Helvetica-Bold", 11)
    p.drawString(margin, y, "Code")
    p.drawString(margin + 130, y, "Subject Name")
    p.drawString(width - margin - 50, y, "Marks")
    y -= 15
    p.line(margin, y, width - margin, y)
    y -= 20

    # Table Rows
    p.setFont("Helvetica", 11)
    for sub in subjects:
        p.drawString(margin, y, sub["code"])
        p.drawString(margin + 130, y, sub["name"])
        p.drawString(width - margin - 50, y, str(result["marks"].get(sub["code"], "-")))
        y -= 18

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name=f"{student['reg_no']}_result.pdf",
                     mimetype="application/pdf")

# ------------------ Admin View / Edit / Delete ------------------
@student_bp.route("/admin/student/<reg_no>")
def admin_view_student(reg_no):
    if not is_admin():
        return redirect(url_for("auth.login"))
    student = get_student(reg_no)
    result = get_marks(reg_no)
    return render_template("student_profile.html", student=student, result=result)

@student_bp.route("/admin/student/<reg_no>/edit", methods=["POST"])
def admin_edit_student(reg_no):
    name = request.form.get("name")
    dept = request.form.get("dept")
    year = request.form.get("year")
    password = request.form.get("password")

    photo_file = request.files.get("photo")
    photo_filename = None
    if photo_file and allowed_file(photo_file.filename):
        photo_filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
        photo_file.save(photo_path)

    update_student(reg_no, name, dept, year, photo_filename)
    if password:
        update_student_password(reg_no, password)

    flash("✅ Student updated successfully.", "success")
    return redirect(url_for("students.admin_view_student", reg_no=reg_no))

@student_bp.route("/admin/student/<reg_no>/delete", methods=["POST"])
def admin_delete_student(reg_no):
    delete_student(reg_no)
    flash("❌ Student deleted.", "danger")
    return redirect(url_for("students.admin_students"))
