# Face Recognition OSS Team 11.
This is face recognition program based on open CV. It uses YuNet as a face detector, and sface as a face recognizer. It supports GUI. You still need to run this code on CLI, however.
# License
- yunet.py and face_detection_yunet_2022mar.onnx are licensed under the MIT license.
- eye-outline.ico is from ionicons, link in Reference. Original svg file was converted to ico. MIT licencse
- Other files are licensed under the Apache 2.0.
- I do NOT own the file that not made by myself. Before Use this project, check for the licence of each file.
## Feature
- GUI
- face registration
- face recognition
- delete face data
- log on log.csv
# Demo
[![Youtube demo Video](http://img.youtube.com/vi/nQ3bf4chPDQ/0.jpg)](https://youtu.be/nQ3bf4chPDQ)  
click image to View demo video.
![Logimage](https://user-images.githubusercontent.com/100254362/206968705-610e8edb-0308-4581-ab95-4b1265a2a40c.jpg)

photo by Spencer Selover, Mateus Souza, Yogendra Singh
- Type name into input box and click Registration to add new face. The program waits 3 seconds and capture the image.
- click Recognition to Recognize face. The program will show name.
- Type name into iunput box and click Delete data. It will delete name's face data.
- Logs are saved in log.csv
# Install
**This program do not supports MacOS. Please use Windows 10/11 only. I highly recommend you to use Windows 11 on AMD64(x86_64)**
1. Install miniconda 3. https://docs.conda.io/en/latest/miniconda.html
2. Run anaconda prompt
3. Download the project.
4. Go to the project file directory that you downloaded.
5. Make a new environment on Anaconda Prompt and activate it.
```
conda create -n NAME_YOU_WANT python=3.8

conda activate NAME_YOU_WANT
```
6. Run below code on Anaconda Prompt (miniconda3)
```
python install.py
```
7. Run main program
```
python main.py RESOLUTION_YOU_WANT
```
# FAQ
Q: It doesn't work.  
A: You can try these steps.  
1. Delete log.csv and data.txt file.
2. Try it on better PC.
3. Re install the program.  
  If the program doesn't work after these steps, contact me that I can solve this problem.

Q: It doesn't recognize faces.  
A: There are some causes.  
1. Too bright or too dark.
2. Camera is not good enough.
3. The person changed too much to recognize.
4. Camera is changed.

# Reference
- https://foss4g.tistory.com/1502
- https://docs.python.org/3/library/tk.html
- https://pillow.readthedocs.io/en/stable/installation.html
- https://github.com/opencv/opencv_zoo/tree/master/models/face_detection_yunet
- https://github.com/opencv/opencv_zoo/tree/master/models/face_recognition_sface
- https://github.com/ionic-team/ionicons
