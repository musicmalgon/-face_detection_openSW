# OSS term project code.
# 202234900 Seol Jaemin(blackseol@gachon.ac.kr)
import tkinter
from PIL import ImageTk, Image
import cv2
import os
#global
vidWidth = 1280
vidHeight = 720
#window
win = tkinter.Tk()
win.configure(background="white")
win.title("Face-recognition")
win.geometry("1280x800")
win.resizable(True, True)

videoFrame = tkinter.Frame(win, bg = "black", width=1280, height=720)
videoFrame.grid(row=1, column=0)

videolb = tkinter.Label(win, width=1280, height=720)
videolb.grid(row=1, column=0)

video = cv2.VideoCapture(0)
video.set(4, 720)
video.set(3, 1280)
#video
def videoShow():
    global vidWidth
    global vidHeight
    status, frame = video.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(frame)
    img.resize((vidWidth, vidHeight))
    imgtk = ImageTk.PhotoImage(image=img)

    videolb.image = imgtk
    videolb.configure(image=imgtk)
    videolb.after(16, videoShow)

#labels
#top text
topText = tkinter.Label(win, text="Recognizing faces...", bg="white")
topText.grid(row=0, column=0)

def resize():
    global vidWidth
    global vidHeight 
    newWidth = win.winfo_width()
    newHeight = win.winfo_height()
    vidWidth = newWidth
    vidHeight = newHeight
    videoFrame.config(width=newWidth, height=newHeight)
    videolb.config(width=newWidth, height=newHeight)
    win.after(16, resize)

videoShow()
#resize()
win.mainloop()
