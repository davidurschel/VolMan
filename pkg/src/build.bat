@echo off
set PYINSTALLER=pyinstaller
set SPEC_FILE1=VolMan.spec
set SPEC_FILE2=VolMan_Config_Editor.spec
set CONFIG_FILE=config.cfg
set DIST_DIR=dist

%PYINSTALLER% %SPEC_FILE1%

if exist %DIST_DIR% (
    echo %SPEC_FILE1% build completed.
) else (
    echo %DIST_DIR% directory not found after %SPEC_FILE1% build. Exiting.
    exit /b 1
)

%PYINSTALLER% %SPEC_FILE2%

if exist %DIST_DIR% (
    echo %SPEC_FILE2% build completed.
) else (
    echo %DIST_DIR% directory not found after %SPEC_FILE2% build. Exiting.
    exit /b 1
)

copy %CONFIG_FILE% %DIST_DIR%\
echo Configuration file copied to %DIST_DIR%.

pause
