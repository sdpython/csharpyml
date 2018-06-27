@echo off
set PATH=%PATH%;c:\Python365_x64
set PYTHONPATH=%~dp0..\pyquickhelper\src

cd cscode\machinelearning
if exist bin\x64.Release goto mldeb:
@echo [build.cmd] build machinelearning release
cmd /C build.cmd -release
if %errorlevel% neq 0 exit /b %errorlevel%
:mldeb:
if exist bin\x64.Debug goto mlrel:
@echo [build.cmd] build machinelearning debug
cmd /C build.cmd -debug
if %errorlevel% neq 0 exit /b %errorlevel%
:mlrel:
cd ..\..

if not exist cscode\machinelearning\bin\x64.Debug goto copymlrel:
@echo [build.cmd] copy binaries for machinelearning
python -u setup.py copybinml debug
if %errorlevel% neq 0 exit /b %errorlevel%
:copymlrel:
if not exist cscode\machinelearning\bin\x64.Release goto copybin:
python -u setup.py copybinml release
if %errorlevel% neq 0 exit /b %errorlevel%

:copybin:
@echo [build.cmd] build machinelearningext
cd cscode\machinelearningext\machinelearningext
dotnet build -c Release machinelearningext.sln
if %errorlevel% neq 0 exit /b %errorlevel%
dotnet build -c debug machinelearningext.sln
if %errorlevel% neq 0 exit /b %errorlevel%
cd ..\..\..

@echo [build.cmd] copy binaries for machinelearningext
python -u setup.py copybinmlext debug
if %errorlevel% neq 0 exit /b %errorlevel%
python -u setup.py copybinmlext release
if %errorlevel% neq 0 exit /b %errorlevel%

@echo [build.cmd] build CSharPyMLExtension_netcore
cd cscode
cmd /C dotnet build -c Release CSharPyMLExtension_netcore.sln
if %errorlevel% neq 0 exit /b %errorlevel%
cmd /C dotnet build -c Debug CSharPyMLExtension_netcore.sln
if %errorlevel% neq 0 exit /b %errorlevel%
cd ..

@echo [build.cmd] copy binaries
python -u setup.py copybin debug
if %errorlevel% neq 0 exit /b %errorlevel%
python -u setup.py copybin release
if %errorlevel% neq 0 exit /b %errorlevel%


:end:
@echo [build.cmd] Completed.

