@echo off

set /p filename=Please input file path:
set /p segment_time=Please input split time:

for %%F in ("%filename%") do (
set "output_path=%%~dpF"
set "output_filename=%%~nF"
)

ffmpeg -i "%filename%" -f segment -segment_time %segment_time% -c copy "%output_path%splited_%output_filename%"_"%%01d.wav"

pause