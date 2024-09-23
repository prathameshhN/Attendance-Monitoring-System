import sqlite3
import datetime
import time

class AttendanceModule:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.attendance_dict = {}

    def mark_attendance(self, user_id, timestamp):
        if user_id not in self.attendance_dict:
            self.attendance_dict[user_id] = [timestamp]
        else:
            self.attendance_dict[user_id].append(timestamp)

    def add_student(self, student_id, student_name):
        self.cursor.execute("INSERT INTO students (id, name) VALUES (?, ?)", (student_id, student_name))
        self.conn.commit()

    def remove_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.conn.commit()

    def get_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def calculate_attendance_percentage(self, student_id):
        self.cursor.execute("SELECT COUNT(*) FROM attendance WHERE user_id = ?", (student_id,))
        total_attendance = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM attendance")
        total_days = self.cursor.fetchone()[0]
        return (total_attendance / total_days) * 100

    def close_db(self):
        self.conn.close()

    def process_attendance(self):
        for user_id, timestamps in self.attendance_dict.items():
            if len(timestamps) >= 2:
                self.cursor.execute("INSERT INTO attendance (user_id, timestamp) VALUES (?, ?)", (user_id, timestamps[0]))
                self.conn.commit()
        self.attendance_dict = {}

def run_attendance_system():
    attendance_module = AttendanceModule("attendance.db")
    camera_module = CameraModule()
    image_processing_module = ImageProcessingModule("known_faces")

    for _ in range(4):
        timestamp = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(0, 55))
        while datetime.datetime.now() < timestamp:
            img = camera_module.capture_image()
            if img is not None:
                identified_faces = image_processing_module.identify_faces(img)
                for user_id in identified_faces:
                    attendance_module.mark_attendance(user_id, timestamp)
        attendance_module.process_attendance()
        time.sleep(60)

if __name__ == "__main__":
    run_attendance_system()