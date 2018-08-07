@echo off
set ppythonpath="c:\Python370_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python366_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python365_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python364_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python363_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python36_x64"

set PATH=%PATH%;%ppythonpath%
set PYTHONPATH=%~dp0..\pyquickhelper\src


@echo [build_short.cmd] build CSharPyMLExtension_netcore
cd cscode
cmd /C dotnet build -c Release CSharPyMLExtension_netcore.sln
if %errorlevel% neq 0 exit /b %errorlevel%
cmd /C dotnet build -c Debug CSharPyMLExtension_netcore.sln
if %errorlevel% neq 0 exit /b %errorlevel%
cd ..

@echo [build_short.cmd] copy binaries
python -u setup.py copybin debug
if %errorlevel% neq 0 exit /b %errorlevel%
python -u setup.py copybin release
if %errorlevel% neq 0 exit /b %errorlevel%


:end:
@echo [build_short.cmd] Completed.

