#!/usr/bin/python
import subprocess
import threading
import time
import glob
import os
import numpy as np
import cv2

#print(os.listdir("."))
EXTRACTED_FRAME_DIR = "./frame_extraction_ws"
EXTRACTED_FACE_DIR  = "./face_extraction_ws"
lib_relative_path = 'extlib/haarcascades/'
MOVIES_DIR = "./movies"
videoSuffix = ["mp4", "mkv"]
frameExtractionThreadPool = []
face_cascade = cv2.CascadeClassifier(lib_relative_path + 'haarcascade_frontalface_default.xml')
class Video:
    
    def __init__ (self, fileName):
        self.mVideoNameFull = fileName
        if ("." in fileName):
            self.mVideoNameWOSuffix = fileName[0:fileName.index(".")]
        else:
            self.mVideoNameWOSuffix = fileName
        
    def PrintVideoName(self):
        print(self.mVideoNameWOSuffix)
        
    def GetVideoNameFull(self):
        return self.mVideoNameFull
        
    def GetVideoNameWOSuffix(self):
        return self.mVideoNameWOSuffix
        
class FrameExtractionThread (threading.Thread):
    def __init__ (self, video):
        threading.Thread.__init__(self)
        self.mVideo = video
    
    def run(self):
        try:
            print("Frame Extraction:\n")
            self.mVideo.PrintVideoName()
            if (not os.path.isdir(EXTRACTED_FRAME_DIR + "/" + self.mVideo.GetVideoNameWOSuffix())):
                subprocess.call("mkdir " + EXTRACTED_FRAME_DIR + "/" + self.mVideo.GetVideoNameWOSuffix(), shell = True)
            systemCallCMD = "ffmpeg -i " + MOVIES_DIR + "/" + self.mVideo.GetVideoNameFull() + " -vf fps=1 " + EXTRACTED_FRAME_DIR + "/" + self.mVideo.GetVideoNameWOSuffix() + "/" + self.mVideo.GetVideoNameWOSuffix() + "%010d.png"
            subprocess.check_output(systemCallCMD, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as ex:
            print(ex.output)
            
class FaceDetectionThread (threading.Thread):
    def __init__ (self, video):
        threading.Thread.__init__(self)
        self.mVideo = video
        
    def run(self):
        try:
            face_cascade = cv2.CascadeClassifier(lib_relative_path + 'haarcascade_frontalface_default.xml')
            self.mVideo.PrintVideoName()
            print(EXTRACTED_FACE_DIR + "/" + self.mVideo.GetVideoNameWOSuffix())
            if (not os.path.isdir(EXTRACTED_FACE_DIR + "/" + self.mVideo.GetVideoNameWOSuffix())):
                subprocess.call("mkdir " + EXTRACTED_FACE_DIR + "/" + self.mVideo.GetVideoNameWOSuffix(), shell = True)
                
            for frame in os.listdir(EXTRACTED_FRAME_DIR + "/" + self.mVideo.GetVideoNameWOSuffix()):
                framename = frame.split(".")[0]
                img = cv2.imread(EXTRACTED_FRAME_DIR + "/" + self.mVideo.GetVideoNameWOSuffix() + "/" + frame)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 5)

                for (x,y,w,h) in faces:
                    h = h + 50
                    w = w + 50
                    x = x - 10
                    y = y - 10
                    roi_color = img[y:y+h, x:x+w]
                    cv2.imwrite(EXTRACTED_FACE_DIR + "/" + self.mVideo.GetVideoNameWOSuffix() + "/" + framename + "_roi.png", roi_color)
                    
        except subprocess.CalledProcessError as ex:
            print(ex.output)
        
def CheckIfVideoFile( fileName ):
    found = False
    for item in videoSuffix:
        if (item in fileName):
            found = True
            return found
    return found
'''
if (not (os.path.isdir(MOVIES_DIR) or os.path.isdir(EXTRACTED_FRAME_DIR))):
    print("Derectory not found.")
    exit(1)

for item in os.listdir(MOVIES_DIR):
    if (CheckIfVideoFile(item)):
        frameExtractionThreadPool.append(FrameExtractionThread(Video(item)))

print("Starting Extraction Threads")

for thread in frameExtractionThreadPool:
    thread.start()
    

for thread in frameExtractionThreadPool:
    thread.join()

print("Starting to process face detection")

for item in os.listdir(EXTRACTED_FRAME_DIR):
    frameExtractionThreadPool.append(FaceDetectionThread(Video(item)))
    
for thread in frameExtractionThreadPool:
    thread.start()
    

for thread in frameExtractionThreadPool:
    thread.join()


for item in os.listdir(EXTRACTED_FRAME_DIR):
    if (not os.path.isdir(EXTRACTED_FACE_DIR + "/" + item)):
        subprocess.call("mkdir " + EXTRACTED_FACE_DIR + "/" + item, shell = True)
    
    for frame in os.listdir(EXTRACTED_FRAME_DIR + "/" + item):
        framename = frame.split(".")[0]
        img = cv2.imread(EXTRACTED_FRAME_DIR + "/" + item + "/" + frame)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        print(len(faces))

        for (x,y,w,h) in faces:
            h = h + 50
            w = w + 50
            x = x - 10
            y = y - 10
            roi_color = img[y:y+h, x:x+w]
            cv2.imwrite(EXTRACTED_FACE_DIR + "/" + item + "/" + framename + "_roi.png", roi_color)
    
print("All threads joined")


executionOutput = ""
try:
    for video in videoArray:
        video.PrintVideoName()
        systemCallCMD = "ffmpeg -i " + video.GetVideoNameFull() + " -vf fps=1/600 " + video.GetVideoNameWOSuffix() + "%03d.png"
        executionOutput = subprocess.check_output(systemCallCMD, stderr=subprocess.STDOUT, shell=True)
        
except subprocess.CalledProcessError as ex:
        print ex.output
''' 
