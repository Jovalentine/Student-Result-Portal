**📘 Student Result Management System**

A modern, secure, and fully functional web-based portal built using Flask + MongoDB, designed for colleges to manage student profiles, academic records, and result generation.
The system includes separate interfaces for Admin and Students, allowing easy management, result viewing, and PDF result downloads.

**🚀 Features
👨‍🏫 Admin Module**

1.Add, update, and delete students
2.Upload student profile photos
3.Manage subjects based on departments
4.Enter and update marks
5.View complete student profiles with results
6.Auto-generate PDF result sheets
7.Stylish UI with modern responsive layout

**🎓 Student Module**

1.Student login using register number
2.Profile dashboard with photo
3.View complete result sheet
4.Download result as PDF
5.Secure session-based access

**🏛 Tech Stack**

Backend: Flask (Python)
Database: MongoDB
Frontend: HTML5, CSS3, Jinja2 Templates
PDF Generation: ReportLab
Server: Gunicorn/Nginx (optional for deployment)

**🔧 Installation & Setup**
1️⃣ Clone the repository
git clone https://github.com/Jovalentine/Student-Result-Portal.git
cd Student-Result-Portal
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the app
python app.py

Your application will run at: http://127.0.0.1:5000/

**🛡 Admin Login**

Default credentials (change later):

username: admin  
password: admin123

**📄 PDF Result Generator**

Each student can download their result as a professionally formatted PDF including:

1.Student photo
2.Marks table
3.Total, percentage, pass/fail
4.College branding
5.Auto page breaks (for many subjects)
