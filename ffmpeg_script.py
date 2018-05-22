#!/usr/bin/python
import subprocess
import threading
import time
import os
import numpy as np
import cv2
from script import Video, FrameExtractionThread, CheckIfVideoFile


EXTRACTED_FRAME_DIR = "./frame_extraction_ws"
EXTRACTED_FACE_DIR  = "./face_extraction_ws"
lib_relative_path = 'extlib/haarcascades/'
MOVIES_DIR = "./movies"
videoSuffix = ["mp4", "mkv"]
frameExtractionThreadPool = []

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