import cv2
import face_recognition
import mysql.connector
from tkinter import Tk, Label, Button, messagebox, Entry, StringVar, OptionMenu
from tkinter import ttk
from datetime import datetime
import hashlib
import os

# MySQL database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Dadaso@123',
    'database': 'attendance_management'
}

# Create a connection to the MySQL database
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

# Create the attendance management database and tables if they don't exist
def create_database():
    query = "CREATE DATABASE IF NOT EXISTS attendance_management"
    cursor.execute(query)
    cnx.commit()

    query = "CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT, name VARCHAR(255), roll_number VARCHAR(255), email VARCHAR(255), PRIMARY KEY (id))"
    cursor.execute(query)
    cnx.commit()

    query = "CREATE TABLE IF NOT EXISTS faculty (id INT AUTO_INCREMENT, name VARCHAR(255), email VARCHAR(255), PRIMARY KEY (id))"
    cursor.execute(query)
    cnx.commit()

    query = "CREATE TABLE IF NOT EXISTS admin (id INT AUTO_INCREMENT, name VARCHAR(255), email VARCHAR(255), PRIMARY KEY (id))"
    cursor.execute(query)
    cnx.commit()

    query = "CREATE TABLE IF NOT EXISTS attendance (id INT AUTO_INCREMENT, student_id INT, date DATE, status VARCHAR(255), PRIMARY KEY (id), FOREIGN KEY (student_id) REFERENCES students(id))"
    cursor.execute(query)
    cnx.commit()

    query = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT, username VARCHAR(255), password VARCHAR(255), role VARCHAR(255), PRIMARY KEY (id))"
    cursor.execute(query)
    cnx.commit()

create_database()

# Function to mark attendance
def mark_attendance():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            known_faces = [
                {'name': 'John Doe', 'face_encoding': face_recognition.face_encodings(cv2.imread('john_doe.jpg'))[0]},
                {'name': 'Jane Doe', 'face_encoding': face_recognition.face_encodings(cv2.imread('jane_doe.jpg'))[0]}
            ]

            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_faces[first_match_index]['name']

            query = "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)"
            cursor.execute(query, (1, datetime.now().strftime("%Y-%m-%d"), 'Present'))
            cnx.commit()

            messagebox.showinfo("Attendance", f"Attendance marked for {name}")

        cv2.imshow('Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to generate attendance report
def generate_attendance_report():
    query = "SELECT * FROM attendance"
    cursor.execute(query)
    attendance_data = cursor.fetchall()

    attendance_report = ""
    for attendance in attendance_data:
        attendance_report += f"Student ID: {attendance[1]}, Date: {attendance[2]}, Status: {attendance[3]}\n"

    messagebox.showinfo("Attendance Report", attendance_report)

# Function to add student
def add_student():
    student_name = student_name_entry.get()
    student_roll_number = student_roll_number_entry.get()
    student_email = student_email_entry.get()

    query = "INSERT INTO students (name, roll_number, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (student_name, student_roll_number, student_email))
    cnx.commit()

    messagebox.showinfo("Student Added", f"Student {student_name} added successfully")

# Function to add faculty
def add_faculty():
    faculty_name = faculty_name_entry.get()
    faculty_email = faculty_email_entry.get()

    query = "INSERT INTO faculty (name, email) VALUES (%s, %s)"
    cursor.execute(query, (faculty_name, faculty_email))
    cnx.commit()

    messagebox.showinfo("Faculty Added", f"Faculty {faculty_name} added successfully")

# Function to add admin
def add_admin():
    admin_name = admin_name_entry.get()
    admin_email = admin_email_entry.get 
# Function to add admin
def add_admin():
    admin_name = admin_name_entry.get()
    admin_email = admin_email_entry.get()

    query = "INSERT INTO admin (name, email) VALUES (%s, %s)"
    cursor.execute(query, (admin_name, admin_email))
    cnx.commit()

    messagebox.showinfo("Admin Added", f"Admin {admin_name} added successfully")

# Function to register user
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    role = role_var.get()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, hashed_password, role))
    cnx.commit()

    messagebox.showinfo("User  Registered", f"User  {username} registered successfully")

# Function to login user
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, hashed_password))
    user_data = cursor.fetchone()

    if user_data:
        messagebox.showinfo("Login Successful", f"Welcome {username}")
        login_frame.pack_forget()
        mark_attendance_button.pack()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to reset password
def reset_password():
    username = username_entry.get()
    old_password = old_password_entry.get()
    new_password = new_password_entry.get()

    hashed_old_password = hashlib.sha256(old_password.encode()).hexdigest()
    hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, hashed_old_password))
    user_data = cursor.fetchone()

    if user_data:
        query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(query, (hashed_new_password, username))
        cnx.commit()

        messagebox.showinfo("Password Reset", f"Password reset successfully for {username}")
    else:
        messagebox.showerror("Password Reset Failed", "Invalid username or password")

# Function to view user profile
def view_user_profile():
    username = username_entry.get()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()

    if user_data:
        messagebox.showinfo("User  Profile", f"Username: {user_data[1]}\nRole: {user_data[3]}")
    else:
        messagebox.showerror("User  Profile Not Found", "Invalid username")

# Create the GUI
root = Tk()
root.title("Attendance Management System")

# Create the label and button for marking attendance
label = Label(root, text="Attendance Management System")
label.pack()

# Create the section for adding students
student_frame = ttk.LabelFrame(root, text="Add Student")
student_frame.pack(padx=10, pady=10)

student_name_label = Label(student_frame, text="Name:")
student_name_label.grid(row=0, column=0)
student_name_entry = Entry(student_frame)
student_name_entry.grid(row=0, column=1)

student_roll_number_label = Label(student_frame, text="Roll Number:")
student_roll_number_label.grid(row=1, column=0)
student_roll_number_entry = Entry(student_frame)
student_roll_number_entry.grid(row=1, column=1)

student_email_label = Label(student_frame, text="Email:")
student_email_label.grid(row=2, column=0)
student_email_entry = Entry(student_frame)
student_email_entry.grid(row=2, column=1)

add_student_button = Button(student_frame, text="Add Student", command=add_student)
add_student_button.grid(row=3, columnspan=2)

# Create the section for adding faculty
faculty_frame = ttk.LabelFrame(root, text="Add Faculty")
faculty_frame.pack(padx=10, pady=10)

faculty_name_label = Label(faculty_frame, text="Name:")
faculty_name_label.grid(row=0, column=0)
faculty_name_entry = Entry(faculty_frame)
faculty_name_entry.grid(row=0, column=1)

faculty_email_label = Label(faculty_frame, text="Email:")
faculty_email_label.grid(row=1, column=0)
faculty_email_entry = Entry(faculty_frame)
faculty_email_entry.grid(row=1, column=1)

add_faculty_button = Button(faculty_frame, text="Add Faculty", command=add_faculty)
add_faculty_button.grid(row=2, columnspan=2)

# Create the section for adding admin
admin_frame = ttk
# Create the section for adding admin
admin_frame = ttk.LabelFrame(root, text="Add Admin")
admin_frame.pack(padx=10, pady=10)

admin_name_label = Label(admin_frame, text="Name:")
admin_name_label.grid(row=0, column=0)
admin_name_entry = Entry(admin_frame)
admin_name_entry.grid(row=0, column=1)

admin_email_label = Label(admin_frame, text="Email:")
admin_email_label.grid(row=1, column=0)
admin_email_entry = Entry(admin_frame)
admin_email_entry.grid(row=1, column=1)

add_admin_button = Button(admin_frame, text="Add Admin", command=add_admin)
add_admin_button.grid(row=2, columnspan=2)

# Create the section for user registration
registration_frame = ttk.LabelFrame(root, text="Register User")
registration_frame.pack(padx=10, pady=10)

username_label = Label(registration_frame, text="Username:")
username_label.grid(row=0, column=0)
username_entry = Entry(registration_frame)
username_entry.grid(row=0, column=1)

password_label = Label(registration_frame, text="Password:")
password_label.grid(row=1, column=0)
password_entry = Entry(registration_frame, show="*")
password_entry.grid(row=1, column=1)

role_var = StringVar(registration_frame)
role_var.set("Student")
role_option = OptionMenu(registration_frame, role_var, "Student", "Faculty", "Admin")
role_option.grid(row=2, column=0)

register_button = Button(registration_frame, text="Register", command=register_user)
register_button.grid(row=2, column=1)

# Create the section for user login
login_frame = ttk.LabelFrame(root, text="Login User")
login_frame.pack(padx=10, pady=10)

username_label = Label(login_frame, text="Username:")
username_label.grid(row=0, column=0)
username_entry = Entry(login_frame)
username_entry.grid(row=0, column=1)

password_label = Label(login_frame, text="Password:")
password_label.grid(row=1, column=0)
password_entry = Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

login_button = Button(login_frame, text="Login", command=login_user)
login_button.grid(row=2, columnspan=2)

mark_attendance_button = Button(root, text="Mark Attendance", command=mark_attendance)
mark_attendance_button.pack_forget()

# Create the section for password reset
reset_frame = ttk.LabelFrame(root, text="Reset Password")
reset_frame.pack(padx=10, pady=10)

username_label = Label(reset_frame, text="Username:")
username_label.grid(row=0, column=0)
username_entry = Entry(reset_frame)
username_entry.grid(row=0, column=1)

old_password_label = Label(reset_frame, text="Old Password:")
old_password_label.grid(row=1, column=0)
old_password_entry = Entry(reset_frame, show="*")
old_password_entry.grid(row=1, column=1)

new_password_label = Label(reset_frame, text="New Password:")
new_password_label.grid(row=2, column=0)
new_password_entry = Entry(reset_frame, show="*")
new_password_entry.grid(row=2, column=1)

reset_button = Button(reset_frame, text="Reset", command=reset_password)
reset_button.grid(row=3, columnspan=2)

# Create the section for viewing user profile
profile_frame = ttk.LabelFrame(root, text="View User Profile")
profile_frame.pack(padx=10, pady=10)

username_label = Label(profile_frame, text="Username:")
username_label.grid(row=0, column=0)
username_entry = Entry(profile_frame)
username_entry.grid(row=0, column=1)

view_button = Button(profile_frame, text="View", command=view_user_profile)
view_button.grid(row=1, columnspan=2)

# Create the button for generating attendance report
report_button = Button(root, text="Generate Attendance Report", command=generate_attendance_report)
report_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
