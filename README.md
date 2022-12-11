# Face Recognition OSS Team 11.
This is face recognition program based on open CV. It uses YuNet as a face detector, and sface as a face recognizer. It supports GUI. You still need to run this code on CLI, however.
## Feature
- GUI
- face registration
- face recognition
- delete face data.
- log on log.csv
# Demo
- working on it
# How to use
1. Install miniconda 3. https://docs.conda.io/en/latest/miniconda.html
2. Run anaconda prompt
3. Download the project.
4. Go to the project file directory that you downloaded.
5. Make a new environment on Anaconda Prompt and activate it.
```
conda create -n NAME_YOU_WANT

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

# References
- https://foss4g.tistory.com/1502
- https://docs.python.org/3/library/tk.html
- https://pillow.readthedocs.io/en/stable/installation.html
- https://github.com/opencv/opencv_zoo/tree/master/models/face_detection_yunet
- https://github.com/opencv/opencv_zoo/tree/master/models/face_recognition_sface