# OSS term project code.
# 202234900 Seol Jaemin(blackseol@gachon.ac.kr)

import tkinter
from PIL import ImageTk, Image
import cv2
import os
#window
win = tkinter.Tk()
win.title("Face-recognition")
win.geometry("1280x800")
win.resizable(False, False)
videoFrame = tkinter.Frame(win, bg = "white", width=1280, height=720)
videoFrame.grid(row=1, column=0)

videolb = tkinter.Label(win)
videolb.grid(row=0, column=0)
video = cv2.VideoCapture(0)

video.set(4, 720)
video.set(3, 1280)
#video
def video_show():

    status, frame = video.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)

    videolb.imgtk = imgtk
    videolb.configure(image=imgtk)
    videolb.after(10, video_show)

video_show()
win.mainloop()