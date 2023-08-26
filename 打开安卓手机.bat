@echo off
E:/scrcpy-win64-v2.1.1/adb.exe connect 192.168.1.1:5555
E:/scrcpy-win64-v2.1.1/scrcpy.exe -s 192.168.1.1:5555 --turn-screen-off
pause