# OSS term project code.
# Face recognition with open CV
# 202234900 Seol Jaemin(blackseol@gachon.ac.kr)
print("Loading... Please wait...")
import os
import sys
import argparse
import warnings
import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
import cv2 as cv
from yunet import YuNet
from sface import SFace
#argparse
parser = argparse.ArgumentParser(description="Face detection and recognition using open CV.\
\n2022. Gachon Univ. OSS team 11.\n202234900 Seol Jaemin\n2022*****NAMEHERE\n2022*****NAMEHERE\n2022*****NAMEHERE")
parser.add_argument('resolution', help="vertical resolution of window in interger", action="store")
parser.add_argument('-c', '--camera', help="camera number.", dest="camera_number" ,action="store", default=0)
parser.add_argument('-l', '--lowSpec', help="Use this option if you are using low spec PC", action="store_true", default=False)
parser.add_argument('-w', '--showWarning', help="enables warning message", action="store_true", default=False)
parser.add_argument('--cuda', help="use Nvidia gpu accelleratioin", action="store_true", default=False)

args = parser.parse_args()
#setup variables
try:
    vres = int(args.resolution)
    hres = int((vres / 9) * 16)
    bres = vres - int(vres * 0.9)
    geoStr = "{}x{}".format(hres, vres)
    camNum = args.camera_number
    if args.lowSpec:
        dtime = 33
    else:
        dtime = 16

    if args.showWarning:
        pass
    else:
        #disable warning to show custom warning message only.
        warnings.filterwarnings("ignore")
    sfacePath = "face_recognition_sface_2021dec.onnx"
    yunetPath = "face_detection_yunet_2022mar.onnx"
    if args.cuda:
        backID = cv.dnn.DNN_BACKEND_CUDA
        targID = cv.dnn.DNN_TARGET_CUDA
    else:
        backID = cv.dnn.DNN_BACKEND_OPENCV
        targID = cv.dnn.DNN_TARGET_CPU
except:
    print("Program init failed.")
    os.system('python main.py -h')
    sys.exit(1)
#window
win = tk.Tk()
win.configure(background="white")
win.title("Face-recognition")
win.geometry(geoStr)
win.resizable(False, False)

videoFrame = tk.Frame(win, bg = "black", width=hres, height=vres - bres)
videoFrame.grid(row=1, column=0)

videolb = tk.Label(win, width=hres, height=vres - bres)
videolb.grid(row=1, column=0)
try:
    video = cv.VideoCapture(camNum + cv.CAP_DSHOW)
    #maximun resolution
    video.set(3, 100000)
    video.set(4, 100000)
    videoHres = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    videoVres = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
except:
    print("Camera access failed.\n1. Close other apps that uses camera.\n"+\
                "2. Check if camera is connected.\n"+\
                "3. Check 'Privacy & security' setting.")
    sys.exit(1)

#init face detector and recognizer
detector = YuNet(modelPath=yunetPath,
                inputSize=[videoHres, videoVres],
                confThreshold=0.9,
                nmsThreshold=0.3,
                topK=5000,
                backendId=backID,
                targetId=targID)
recognizer = SFace(modelPath=sfacePath, disType=0, backendId=backID, targetId=targID)
#functions
def close(e):
    win.destroy()
win.bind("<Escape>", close)

def videoGUI():
    try:
        status, frame = video.read()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        resizeRatio = (vres-bres)/videoVres
        frame = cv.resize(frame, (int(videoHres*resizeRatio), vres-bres))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        videolb.image = imgtk
        videolb.configure(image=imgtk)
    except:
        print("Image processing failed.\nTry for using other camera or higher program resolution.")
        sys.exit(1)
    videolb.after(dtime, videoGUI)

def faceRecognition():
    status, frame = video.read()


#labels
#top text
topText = tk.Label(win, text="Please select task to do", bg="white")
topText.grid(row=0, column=0)
#face registration button
def faceRecognition():
    status, frame = video.read()


videoGUI()
win.mainloop()
