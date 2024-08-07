@echo off
REM Define variables
set PYINSTALLER=pyinstaller
set SPEC_FILE=VolMan.spec
set CONFIG_FILE=config.cfg
set DIST_DIR=dist

REM Build the executable
%PYINSTALLER% %SPEC_FILE%

REM Copy config.cfg into the dist folder
copy %CONFIG_FILE% %DIST_DIR%\
