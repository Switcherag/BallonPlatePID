@echo off
cls
Title Ball on plate Gui
powershell Get-Content "Gui2D\gui_header.txt"


env\python.exe Gui2D/Gui2d.py
pause
START_GUI.bat