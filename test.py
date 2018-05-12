import numpy as np
import cv2
#/pltfrom matplotlib import pyplot as plt

#lib_relative_path = '/home/freeman/Desktop/Shared/extlib/haarcascades/'
lib_relative_path = 'extlib/haarcascades/'
#face_cascade = cv2.CascadeClassifier('/home/freeman/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(lib_relative_path + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(lib_relative_path + 'haarcascade_eye.xml')

#face_cascade = cv2.CascadeClassifier('cv2.haarcascade_frontalface_default.xml')
#img = cv2.imread('xfiles4.jpg')
img = cv2.imread('/home/freeman/Desktop/Shared/nationaltrasure1003.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.2, 5)
print(len(faces))

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
cap = cv2.VideoCapture('Premature.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(24) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''
