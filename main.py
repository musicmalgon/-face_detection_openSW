# OSS term project code.
# Face recognition with open CV
# 202234900 Seol Jaemin(blackseol@gachon.ac.kr)
print("Loading... Please wait...")
import os
import sys
import argparse
import json
import base64
import warnings
from threading import Timer
import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import ImageTk, Image
import cv2 as cv
from yunet import YuNet
from sface import SFace
np.set_printoptions(threshold = sys.maxsize)
#argparse
parser = argparse.ArgumentParser(description="Face detection and recognition using open CV.\
\n2022. Gachon Univ. OSS team 11.\n202234900 Seol Jaemin\n2022*****NAMEHERE\n2022*****NAMEHERE\n2022*****NAMEHERE")
parser.add_argument('resolution', help="vertical resolution of window in interger", action="store")
parser.add_argument('--camera', '-c', help="camera number.", dest="camera_number" ,action="store", default=0)
parser.add_argument('--lowSpec', '-l', help="Use this option if you are using low spec PC", action="store_true", default=False)
parser.add_argument('--showWarning', '-w', help="enables warning message", action="store_true", default=False)
parser.add_argument('--cuda', help="use Nvidia gpu accelleratioin", action="store_true", default=False)
parser.add_argument('--fullScreen', '-f', help="display fullScreen", action="store_true", default=False)

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
if args.fullScreen:
    win.attributes('-fullscreen', True)
else:
    pass

videoFrame = tk.Frame(win, bg = "black", width=hres, height=vres - bres)
videoFrame.place(x=0,y=0)

videolb = tk.Label(win, width=hres, height=vres - bres)
videolb.place(x=0,y=0)
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

count = 4
def faceRegistrationDelay():
    global count
    count = count - 1
    if count <= 0:
        count = 4
        faceRegistration()
        return
    topText.config(text="Face Registration starts in {}...".format(count))
    delay = Timer(1, faceRegistrationDelay)
    delay.start()

def faceRegistration():
    topText.config(text="Please select task to do")
    try:
        status, frame = video.read()
        face = detector.infer(frame)
        faceCount = 0
        for f in (face if face is not None else []):
            faceCount = faceCount + 1
        if faceCount == 1:
            #encode
            status, frame = cv.imencode('.jpg', frame)
            frame = np.array2string(frame)
            frame = frame[1:-1]
            face = np.array2string(face)
            face = face[2:-2]
            #save it on file
            jsonObj = {"img":frame, "detect":face}
            jsonStr = json.dumps(jsonObj)
            jsonStr = jsonStr.replace("\n", " ")
            jsonStr = jsonStr + "\n"
            with open("data.face", "a") as file:
                file.write(jsonStr)

        elif faceCount > 1:
            messagebox.showwarning(title="Face Registration error",
                                    message="Two or more face detected.\nPlease try again.")
        else:
            messagebox.showwarning(title="Face Registration error",
                                    message="Unable to detect face.\nPlease try again.")
    except:
        #print("Face Registration error.\nPleas try again.")
        messagebox.showwarning(title="Face Registration error", message="Please try again.\nIf error continues, reboot the computer")
    else:
        messagebox.showinfo(title="Face Registration success", message="Face Registrated.")

def faceRecognition():
    try:
        with open("data.face", "r") as file:
            jsonStr = file.readline()
            while jsonStr:
                jsonStr = jsonStr.strip()
                jsonObj = json.loads(jsonStr)

                frame = jsonObj['img']
                face = jsonObj['detect']

                frame = frame.split()
                frame = np.array(frame)
                frame = frame.astype(np.uint8)
                frame = cv.imdecode(frame, cv.IMREAD_COLOR)

                face = face.split()
                face = [face]
                face = np.array(face)
                face = face.astype(np.float32)

                #for testing
                img2 = cv.imread("test.jpg")
                face2 = detector.infer(img2)
                result = recognizer.match(frame, face[0][:-1], img2, face2[0][:-1])
        print(result)
    except:
        messagebox.showwarning(title="Face Recognition error", message="Please try it again.\nIf error continues, reboot the computer")
    else:
        pass
def openLog():
    print("openlog")


#labels
#top text
pixelImg = tk.PhotoImage(width=1, height=1)
topText = tk.Label(win, text="Please select task to do", bg="white",width=hres, image=pixelImg, compound="c")
topText.place(x=0,y=0)
#face registration button
btnWidth = int(hres / 3) #3 buttons

faceRegBtn = tk.Button(win, width=btnWidth, height=bres, command=faceRegistrationDelay, text="Registration",
                image=pixelImg, compound="c")
faceRegBtn.place(x=0,y=vres-bres)

faceRecogBtn = tk.Button(win, width=btnWidth, height=bres, command=faceRecognition, text="Recognition",
                image=pixelImg, compound="c")
faceRecogBtn.place(x=btnWidth,y=vres-bres)

openLogBtn = tk.Button(win, width=btnWidth, height=bres, command=openLog, text="Recognition",
                image=pixelImg, compound="c")
openLogBtn.place(x=btnWidth*2,y=vres-bres)

videoGUI()
win.mainloop()
