#!/usr/bin/python
import subprocess
import threading
import time
import os
import numpy as np
import cv2
from script import Video, FaceDetectionThread

EXTRACTED_FRAME_DIR = "./frame_extraction_ws"
EXTRACTED_FACE_DIR  = "./face_extraction_ws"
lib_relative_path = 'extlib/haarcascades/'
MOVIES_DIR = "./movies"
videoSuffix = ["mp4", "mkv"]
faceExtractionThreadPool = []


print("Starting to process face detection")

for item in os.listdir(EXTRACTED_FRAME_DIR):
    faceExtractionThreadPool.append(FaceDetectionThread(Video(item)))
    
for thread in faceExtractionThreadPool:
    thread.start()
    

for thread in faceExtractionThreadPool:
    thread.join()