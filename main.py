# OSS term project code. Team 11.
# Face recognition with open CV
# 202234900 Seol Jaemin(blackseol@gachon.ac.kr)
print("Loading... Please wait...")
import os
import sys
import argparse
import json
import time
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
if os.path.exists("tmp_data.txt"):
    os.remove("tmp_data.txt")
if not os.path.exists("data.txt"):
    file = open("data.txt", "w")
    file.close()
if not os.path.exists("log.csv"):
    with open("log.csv", "w") as file:
        file.write("Time,Name,Activity\n")
#argparse
parser = argparse.ArgumentParser(description="Face detection and recognition using open CV.\
\n2022. Gachon Univ. OSS team 11.\n202234900 Seol Jaemin\n2022*****NAMEHERE\n2022*****NAMEHERE\n2022*****NAMEHERE")
parser.add_argument('resolution', help="vertical resolution of window in interger", action="store")
parser.add_argument('--camera', '-c', help="camera number.", dest="camera_number" ,action="store", default=0)
parser.add_argument('--showWarning', '-w', help="enables warning message", action="store_true", default=False)
parser.add_argument('--fullScreen', '-f', help="display fullScreen", action="store_true", default=False)
args = parser.parse_args()
#setup variables
try:
    vres = int(args.resolution)
    hres = int((vres / 9) * 16)
    bres = vres - int(vres * 0.9)
    geoStr = "{}x{}".format(hres, vres)
    camNum = args.camera_number
    dtime = 16
    if args.showWarning:
        pass
    else:
        #disable warning to show custom warning message only.
        warnings.filterwarnings("ignore")
    sfacePath = "face_recognition_sface_2021dec.onnx"
    yunetPath = "face_detection_yunet_2022mar.onnx"
    backID = cv.dnn.DNN_BACKEND_OPENCV
    targID = cv.dnn.DNN_TARGET_CPU
except:
    print("Program init failed.")
    os.system('python main.py -h') #show help message
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
#video Frame for GUI
videoFrame = tk.Frame(win, bg = "black", width=hres, height=vres - bres)
videoFrame.place(x=0,y=0)
videolb = tk.Label(win, width=hres, height=vres - bres)
videolb.place(x=0,y=0)
try:
    video = cv.VideoCapture(camNum + cv.CAP_DSHOW)
    #maximun resolution
    video.set(3, 100000)
    video.set(4, 100000)
    #get real webcam resolution
    videoHres = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    videoVres = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
except:
    print("Camera access failed.\n1. Close other apps that uses camera.\n"+\
                "2. Check if camera is connected.\n"+\
                "3. Check 'Privacy & security' setting.")
    sys.exit(1)

#init face detector and recognizer
detector = YuNet(modelPath=yunetPath, inputSize=[videoHres, videoVres],
                confThreshold=0.9, nmsThreshold=0.3, topK=5000,
                backendId=backID, targetId=targID)
recognizer = SFace(modelPath=sfacePath, disType=0, backendId=backID, targetId=targID)
#functions
#ESC to close
def close(e):
    win.destroy()
win.bind("<Escape>", close)
#Showing camera video on GUI
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
#Waiting for 3 seconds
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
#registration
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
            jsonObj = {"name":inputBox.get(),"img":frame, "detect":face}
            jsonStr = json.dumps(jsonObj)
            jsonStr = jsonStr.replace("\n", " ")
            jsonStr = jsonStr + "\n"
            with open("data.txt", "a") as file:
                file.write(jsonStr)
            # log
            with open("log.csv", "a") as file:
                file.write(time.strftime("%Y-%m-%d/%H:%M:%S")+","+jsonObj['name']+",registration\n")
            messagebox.showinfo(title="Face Registration success", message="Face Registrated.")
        elif faceCount > 1:
            messagebox.showwarning(title="Face Registration error",
                                    message="Two or more face detected.\nPlease try again.")
        else:
            messagebox.showwarning(title="Face Registration error",
                                    message="Unable to detect face.\nPlease try again.")
    except:
        messagebox.showwarning(title="Face Registration error", message="Please try again.\nIf error continues, reboot the computer")
#recognition
def faceRecognition():
    topText.config(text="Please select task to do")
    try:
        status, frame1 = video.read()
        face1 = detector.infer(frame1)
        faceCount = 0
        for f in (face1 if face1 is not None else []):
            faceCount = faceCount + 1
        if faceCount == 1:
            #read from file
            with open("data.txt", "r") as file:
                jsonStr = file.readline()
                while jsonStr:
                    jsonStr = jsonStr.strip()
                    jsonObj = json.loads(jsonStr)
                    name = jsonObj['name']
                    frame = jsonObj['img']
                    face = jsonObj['detect']
                    #decode
                    frame = frame.split()
                    frame = np.array(frame)
                    frame = frame.astype(np.uint8)
                    frame = cv.imdecode(frame, cv.IMREAD_COLOR)
                    face = face.split()
                    face = [face]
                    face = np.array(face)
                    face = face.astype(np.float32)
                    #recognize
                    result = recognizer.match(frame, face[0][:-1], frame1, face1[0][:-1])
                    if result:
                        messagebox.showinfo(title="Face Recognition success", message="Welcome, {}.".format(name))
                        with open("log.csv", "a") as file: #log
                            logStr = time.strftime("%Y-%m-%d/%H:%M:%S")+","+name+",recognition\n"
                            file.write(logStr)
                        return
                    else:
                        jsonStr = file.readline() #goto next face data
            messagebox.showwarning(title="Face Recognition failed",
                                message="Unregistrated face data.")
        elif faceCount > 1:
            messagebox.showwarning(title="Face Recognition error",
                                    message="Two or more face detected.\nPlease try again.")
        else:
            messagebox.showwarning(title="Face Recognition error",
                                    message="Unable to detect face.\nPlease try again.")
    except:
        messagebox.showwarning(title="Face Recognition error", message="Please try it again.\nIf error continues, reboot the computer")
#delete data
def delData():
    try:
        os.rename("data.txt", "tmp_data.txt") #rename data.txt
        with open("tmp_data.txt", "r") as file: #try to find name
            jsonStr = file.readline()
            while jsonStr:
                jsonStr = jsonStr.strip()
                jsonObj = json.loads(jsonStr)
                if inputBox.get() == jsonObj['name']:
                    delStr = jsonStr
                    break
                else:
                    jsonStr = file.readline()
        if not jsonStr:
            messagebox.showwarning(title="Delete error", message="Can't find name")
            os.rename("tmp_data.txt","data.txt")
            return
        #copy data from tmp_data to data.
        with open("tmp_data.txt", "r") as input:
            with open("data.txt", "w") as output:
                line = input.readline()
                while line:
                    line = line.strip()
                    if line != delStr:
                        output.write(line + "\n")
                        line = input.readline()
                    else: #if we find data to delete, do not copy it
                        line = input.readline()
        if os.path.exists("tmp_data.txt"):
            os.remove("tmp_data.txt")#remove tmp_data
        with open("log.csv", "a") as file:#log
            file.write(time.strftime("%Y-%m-%d/%H:%M:%S")+","+jsonObj['name']+",delete\n")
        messagebox.showinfo(title="Deleted", message="{}'s data is deleted".format(inputBox.get()))
    except:
        messagebox.showwarning(title="Delete error", message="Please try it again.\nIf error continues, reboot the computer")

#labels
#top text
pixelImg = tk.PhotoImage(width=1, height=1)
topText = tk.Label(win, text="Please select task to do", bg="white",width=hres, image=pixelImg, compound="c")
topText.place(x=0,y=0)
#input
inputBox = tk.Entry(win)
inputBox.place(x=0, y=vres-bres-19, width=hres)
#buttons
btnWidth = int(hres / 3) #3 buttons
#face registration button
faceRegBtn = tk.Button(win, width=btnWidth, height=bres, command=faceRegistrationDelay, text="Registration",
                image=pixelImg, compound="c")
faceRegBtn.place(x=0,y=vres-bres)
#face recongnition button
faceRecogBtn = tk.Button(win, width=btnWidth, height=bres, command=faceRecognition, text="Recognition",
                image=pixelImg, compound="c")
faceRecogBtn.place(x=btnWidth,y=vres-bres)
#face recongnition button
deleteBtn = tk.Button(win, width=btnWidth, height=bres, command=delData, text="Delete data",
                image=pixelImg, compound="c")
deleteBtn.place(x=btnWidth*2,y=vres-bres)
#window loop
videoGUI()
win.mainloop()
