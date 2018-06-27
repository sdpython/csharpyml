cd machinelearning
bash build.sh -release
bash build.sh -debug
cd ..

cd machinelearning
bash -c "dotnet publish Microsoft.ML.sln -o ../../dist/Debug -c Debug --self-contained" || true
bash -c "dotnet publish Microsoft.ML.sln -o ../../dist/Release -c Release --self-contained" || true
cd ..

copy machinelearning/bin/x64.Debug/Native/*.dll machinelearning/dist/Debug
copy machinelearning/bin/x64.Release/Native/*.dll machinelearning/dist/Release

cd machinelearningext
dotnet build -c Debug
dotnet build -c Release
cd ..