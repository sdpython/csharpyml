@echo off
set ppythonpath="c:\Python370_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python366_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python365_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python364_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python363_x64"
if not exist %ppythonpath% set ppythonpath="c:\Python36_x64"

set PATH=%PATH%;%ppythonpath%
set PYTHONPATH=%~dp0..\pyquickhelper\src

set DOTNET_CLI_TELEMETRY_OPTOUT=1
set DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
set DOTNET_MULTILEVEL_LOOKUP=0

set LOCALMLEXT=%~dp0..\machinelearningext
if "%1" == "py" goto buildpy:
if exist %LOCALMLEXT% goto copybinaries:

cd cscode\machinelearning
if "%1" == "ml" goto buildml:
if exist bin goto mlend:
@echo [build.cmd] build machinelearning debug and release
:buildml:
cmd /C build.cmd
if %errorlevel% neq 0 exit /b %errorlevel%
:mlend:
cd ..\..

:copybinaries:
if "%1" == "ml" goto copydebug:
if exist cscode\machinelearning\bin\AnyCPU.Debug\Microsoft.ML.Api goto copymlrel:
:copydebug:
@echo [build.cmd] copy debug binaries for machinelearning
python -u setup.py copybinml debug
if %errorlevel% neq 0 exit /b %errorlevel%
:copymlrel:
if "%1" == "ml" goto copyrelease:
if exist cscode\machinelearning\bin\AnyCPU.Release\Microsoft.ML.Api goto copybin:
:copyrelease:
@echo [build.cmd] copy release binaries for machinelearning
python -u setup.py copybinml release
if %errorlevel% neq 0 exit /b %errorlevel%

:copybin:
if exist %LOCALMLEXT% goto copybinariesext:

@echo [build.cmd] build machinelearningext
cd cscode\machinelearningext\machinelearningext
dotnet build -c Release machinelearningext.sln
if %errorlevel% neq 0 exit /b %errorlevel%
dotnet build -c Debug machinelearningext.sln
if %errorlevel% neq 0 exit /b %errorlevel%
cd ..\..\..

:copybinariesext:

@echo [build.cmd] copy binaries for machinelearningext
python -u setup.py copybinmlext debug
if %errorlevel% neq 0 exit /b %errorlevel%
python -u setup.py copybinmlext release
if %errorlevel% neq 0 exit /b %errorlevel%

:buildpy:
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

:finalcopy:

copy cscode\bin\machinelearningext\Release\mkl*.dll cscode\bin\AnyCPU.Release\TestCSharPyMLExtension\netcoreapp2.1
copy cscode\bin\machinelearningext\Debug\mkl*.dll cscode\bin\AnyCPU.Debug\TestCSharPyMLExtension\netcoreapp2.1


:end:
@echo [build.cmd] Completed.

