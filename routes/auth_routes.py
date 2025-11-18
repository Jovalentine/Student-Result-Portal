from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import verify_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        user = verify_user(username, password)

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("students.admin_home"))
            return redirect(url_for("students.student_home", reg_no=user["username"]))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
