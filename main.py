# import cv2
# cap = cv2.VideoCapture(0)
# cap.set(3, 720)
# cap.set(4, 480)
# cv2.waitKey(1000)
# print(cap.get(3))
# print(cap.get(4))
# x = 0
# while True:
#
#     # x += 1
#     success, img = cap.read()
#     cv2.imshow("Face", img)
#     cv2.waitKey(1)
#     if x > 5:
#         break
# cap.release()
# cv2.destroyAllWindows()


# import cv2
#
#
# def test_camera(index):
#     cap = cv2.VideoCapture(index)
#
#     if not cap.isOpened():
#         print(f"Camera {index} not found.")
#         return
#
#     print(f"Testing Camera {index}")
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print(f"Cannot read frame from Camera {index}")
#             break
#
#         cv2.imshow(f"Camera {index}", frame)
#
#         key = cv2.waitKey(1)
#         if key == 27:  # Press 'Esc' to exit
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#
# def main():
#     for index in range(10):  # Try indices 0 to 9
#         test_camera(index)
#
#
# if __name__ == "__main__":
#     main()
#
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
# with open('Attendance1.csv', 'w') as clear_file:
#     clear_file.truncate()

def findEncodings(images):
    encodeList =[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance1.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tString = time_now.strftime('%H:%M')
            dString = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{tString},{dString}')

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('http://100.123.85.56:8080/video')
cap.set(3, 720)
cap.set(4, 480)
while True:
    success, img = cap.read()
    # cv2.waitKey(1)
    # imgS = cv2.r
    # esize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 250, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
    cv2.imshow('cam', img)
    if cv2.waitKey(10) == 13:
        break
cap.release()
cv2.destroyAllWindows()
