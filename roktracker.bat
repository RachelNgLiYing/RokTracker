@echo  off
set /P PORT=Enter PORT:
@echo on
if not exist "output" mkdir output
".\platform-tools\adb.exe" kill-server
".\platform-tools\adb.exe" connect localhost:%PORT%
cd .\
py -3.6 -m pip install --upgrade pip
py -3.6 -m pip install configparser==5.2.0
py -3.6 -m pip install Pillow==8.4.0
py -3.6 -m pip install opencv-python==4.6.0.66
py -3.6 -m pip install -r requirements.txt
py -3.6 -W ignore roktracker_modified_sheets.py
PAUSE
