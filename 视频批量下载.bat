@echo off
setlocal enabledelayedexpansion

REM 提示用户输入下载路径
set /p "output_dir=please enter your output directory: "

REM 检查用户是否输入了下载路径
if "%output_dir%"=="" (
    echo Error: No output directory entered.
    pause
    exit /b
)

REM 创建下载路径
mkdir "%output_dir%" >nul 2>nul

REM 检查是否拖放了文件
if "%~1"=="" (
    echo Error: No file dropped onto the script.
    echo Please drag and drop a text file containing video links onto the script.
    pause
    exit /b
)

REM 读取文本文件
set "file=%~1"

REM 创建临时文件来保存修改后的链接和标题
set "temp_file=%~dpn1_temp%~x1"

REM 下载视频并写入标题到原始文本文件
set "counter=1"
for /f "usebackq delims=" %%A in ("%file%") do (
    echo Downloading: %%A
    for /f "delims=" %%T in ('youtube-dl --get-title "%%A"') do (
        set "title=%%T"
        echo Title: !title!
        youtube-dl -f best --output "%output_dir%\[!counter!] !title!.%%(ext)s" "%%A"
        echo [!counter!] !title! %%A>>"%temp_file%"
        set /a "counter+=1"
    )
)

REM 将临时文件重命名为原始文件
move /y "%temp_file%" "%file%" >nul 2>nul

echo Download completed.
pause
