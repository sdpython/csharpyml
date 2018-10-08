@echo off
set ppythonpath="c:\Python370_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python366_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python365_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python364_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python363_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python36_x64"

set PATH=%PATH%;%ppythonpath%
set PYTHONPATH=%~dp0..\pyquickhelper\src

cd cscode\machinelearning
if "%1" == "ml" goto buildrelease:
if exist bin\x64.Release goto mldeb:
@echo [build.cmd] build machinelearning release
:buildrelease:
cmd /C build.cmd -release
if %errorlevel% neq 0 exit /b %errorlevel%
:mldeb:
if "%1" == "ml" goto builddebug:
if exist bin\x64.Debug goto mlrel:
:builddebug:
@echo [build.cmd] build machinelearning debug
cmd /C build.cmd -debug
if %errorlevel% neq 0 exit /b %errorlevel%
:mlrel:
cd ..\..

if "%1" == "ml" goto copydebug:
if exist cscode\machinelearning\bin\x64.Debug goto copymlrel:
:copydebug:
@echo [build.cmd] copy debug binaries for machinelearning
python -u setup.py copybinml debug
if %errorlevel% neq 0 exit /b %errorlevel%
:copymlrel:
if "%1" == "ml" goto copyrelease:
if exist cscode\machinelearning\bin\x64.Release goto copybin:
:copyrelease:
@echo [build.cmd] copy release binaries for machinelearning
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

