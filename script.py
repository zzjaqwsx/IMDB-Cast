#!/usr/bin/python
import subprocess
import threading
import time
import glob
import os

#print(os.listdir("."))
videoSuffix = ["mp4", "mkv"]
videoArray = []
frameExtractionThreadPool = []
class Video:
    
    def __init__ (self, fileName):
        self.mVideoNameFull = fileName
        self.mVideoNameWOSuffix = fileName[0:item.index(".")]
        
    def PrintVideoName(self):
        print self.mVideoNameWOSuffix
        
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
            self.mVideo.PrintVideoName()
            systemCallCMD = "ffmpeg -i " + self.mVideo.GetVideoNameFull() + " -vf fps=1/600 " + self.mVideo.GetVideoNameWOSuffix() + "%03d.png"
            subprocess.check_output(systemCallCMD, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as ex:
            print ex.output
        


def CheckIfVideoFile( fileName ):
    found = False
    for item in videoSuffix:
        if (item in fileName):
            found = True
            return found
    return found

for item in os.listdir("."):
    if (CheckIfVideoFile(item)):
        videoArray.append(Video(item))
        frameExtractionThreadPool.append(FrameExtractionThread(Video(item)))

print "Starting Extraction Threads"

for thread in frameExtractionThreadPool:
    thread.start()
    

for thread in frameExtractionThreadPool:
    thread.join()
    
print "All threads joined"

'''
executionOutput = ""
try:
    for video in videoArray:
        video.PrintVideoName()
        systemCallCMD = "ffmpeg -i " + video.GetVideoNameFull() + " -vf fps=1/600 " + video.GetVideoNameWOSuffix() + "%03d.png"
        executionOutput = subprocess.check_output(systemCallCMD, stderr=subprocess.STDOUT, shell=True)
        
except subprocess.CalledProcessError as ex:
        print ex.output
''' 
