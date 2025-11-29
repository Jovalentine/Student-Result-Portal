📘 Student Result Management System

A modern, secure, and fully functional web-based portal built using Flask + MongoDB, designed for colleges to manage student profiles, academic records, and result generation.
The system includes separate interfaces for Admin and Students, allowing easy management, result viewing, and PDF result downloads.

🚀 Features
👨‍🏫 Admin Module

Add, update, and delete students

Upload student profile photos

Manage subjects based on departments

Enter and update marks

View complete student profiles with results

Auto-generate PDF result sheets

Stylish UI with modern responsive layout

🎓 Student Module

Student login using register number

Profile dashboard with photo

View complete result sheet

Download result as PDF

Secure session-based access

🏛 Tech Stack

Backend: Flask (Python)

Database: MongoDB

Frontend: HTML5, CSS3, Jinja2 Templates

PDF Generation: ReportLab

Server: Gunicorn/Nginx (optional for deployment)


🔧 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/Jovalentine/Student-Result-Portal.git
cd Student-Result-Portal

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the app
python app.py


Your application will run at:

http://127.0.0.1:5000/

🛡 Admin Login

Default credentials (change later):

username: admin  
password: admin123

📄 PDF Result Generator

Each student can download their result as a professionally formatted PDF including:

Student photo

Marks table

Total, percentage, pass/fail

College branding
Auto page breaks (for many subjects)
