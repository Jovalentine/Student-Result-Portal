from flask import Flask, redirect, url_for
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp

app = Flask(__name__)
app.secret_key = "jo"

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)

@app.route("/")
def root():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
