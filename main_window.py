import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap
import cv2
from camera_module import CameraModule
from image_processing_module import ImageProcessingModule
from attendance_module import AttendanceModule

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Attendance System")
        self.setGeometry(300, 300, 640, 480)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.camera = CameraModule()
        self.image_processing = ImageProcessingModule("known_faces")
        self.attendance = AttendanceModule("attendance.db")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.capture_and_process_image)
        self.timer.start(5000)  

        self.student_list = QComboBox()
        self.layout.addWidget(self.student_list)

        self.update_student_list()

    def capture_and_process_image(self):
        img = self.camera.capture_image()
        if img is not None:
            identified_faces = self.image_processing.identify_faces(img)
            for user_id in identified_faces:
                self.attendance.mark_attendance(user_id)
            self.display_image(img)

    def display_image(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QtGui.QImage(img.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QtGui.QPixmap.fromImage(q_img))

    def update_student_list(self):
        self.student_list.clear()
        students = self.attendance.get_students()
        for student in students:
            self.student_list.addItem(student[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())