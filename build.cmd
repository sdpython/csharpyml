@echo off

@echo [build.cmd] build machinelearning
cd cscode\machinelearning
if exist bin\x64.Release goto mldeb:
cmd /C build.cmd -release
:mldeb:
if exist bin\x64.Debug goto mlrel:
cmd /C build.cmd -debug
:mlrel:
cd ..\..

if not exist cscode\machinelearning\bin\x64.Debug goto end:

@echo [build.cmd] copy binaries for machinelearning
python -u setup.py copybinml debug
python -u setup.py copybinml release

@echo [build.cmd] copy binaries for machinelearning
if not exist cscode\machinelearningext\dist mkdir cscode\machinelearningext\dist
xcopy /Y /S cscode\bin\*.* cscode\machinelearningext\dist

@echo [build.cmd] build machinelearningext
cd cscode\machinelearningext
cmd /C build.cmd -release
cmd /C build.cmd -debug
cd ..\..

@echo [build.cmd] copy binaries for machinelearningext
python -u setup.py copybinmlext debug
python -u setup.py copybinmlext release

@echo [build.cmd] build CSharPyMLExtension_netcore
cd cscode
cmd /C dotnet build -c Release CSharPyMLExtension_netcore.sln
cmd /C dotnet build -c Debug CSharPyMLExtension_netcore.sln
cd ..

:end:
if not exist machinelearning\bin\x64.Debug @echo [build.cmd] Cannot build.
@echo [build.cmd] Completed.

