#202234900 SeolJaemin 2022.
#Gachon univ. (blackseol@gachon.ac.kr)
#auto install libraries to run main program
# Copyright 2022 Jaemin-Seol(jaemin.seol@outlook.com)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
print("""
::::'#######:::'######:::'######::::::::'##::::::'##::::::
:::'##.... ##:'##... ##:'##... ##:::::'####::::'####::::::
::: ##:::: ##: ##:::..:: ##:::..::::::.. ##::::.. ##::::::
::: ##:::: ##:. ######::. ######:::::::: ##:::::: ##::::::
::: ##:::: ##::..... ##::..... ##::::::: ##:::::: ##::::::
::: ##:::: ##:'##::: ##:'##::: ##::::::: ##:::::: ##::::::
:::. #######::. ######::. ######::::::'######::'######::::
::::.......::::......::::......:::::::......:::......:::::
""")
print("""Open Source Software(14511_001) Term Project Team 11.
Face Recognizer with Camera
This python code and main code is intended to run on miniconda3, Windows 11, AMD64(x86_64).
It will automatically install anything you need to run main program.\n
***WARNING!***\nIt may break your development environment.
It is highly recommended to make a new anaconda environment before run this code.
""")
while True:
    isOk = input("Run the code?(y/n):")
    if isOk == 'y':
        break
    elif isOk == 'n':
        os._exit(0)
print("Installing...Please Wait.")
os.system("conda update --all")
os.system("conda install python=3.8.13")
os.system("pip install --upgrade pip")
os.system("pip install opencv-python==4.6.0.66")
os.system("pip install --upgrade Pillow==9.3.0")
print("\nInstalation finished.\nYou can use this command to run main program.")
os.system("python main.py -h")
