@echo off
chcp 65001 >nul
echo ==========================================
echo       Cyber Newton - Windows 环境安装脚本
echo ==========================================

:: 1. 检查 Winget 是否可用
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Winget 工具。
    echo 请手动下载安装以下软件，然后重新运行 setup.bat:
    echo   1. Python 3.10+: https://www.python.org/downloads/
    echo   2. Node.js LTS:  https://nodejs.org/
    echo   3. Git:          https://git-scm.com/
    pause
    exit /b
)

:: 2. 安装 Python
echo.
echo [1/4] 正在安装 Python 3.11...
winget install -e --id Python.Python.3.11 --scope machine

:: 3. 安装 Node.js
echo.
echo [2/4] 正在安装 Node.js LTS...
winget install -e --id OpenJS.NodeJS.LTS

:: 4. 安装 PM2 和 serve
echo.
echo [3/4] 正在安装 PM2...
call npm install -g pm2 serve

echo.
echo ==========================================
echo [成功] 环境安装完成！
echo 请 ***关闭当前窗口*** 并重新打开一个新的 CMD/PowerShell 窗口以生效环境变量。
echo ==========================================
pause