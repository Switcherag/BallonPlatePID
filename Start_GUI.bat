@echo off
cls
Title Ball on plate Gui
powershell Get-Content "Gui2D\gui_header.txt"
echo.

env\Scripts\python.exe Gui2D/Gui2d.py

START_GUI.bat
