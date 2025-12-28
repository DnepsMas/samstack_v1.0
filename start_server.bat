@echo off
chcp 65001 >nul
title Cyber Newton Server (Corrected)

echo ==========================================
echo       [1/3] 检查/安装 后端依赖...
echo ==========================================

:: 1. 检查根目录下的 .venv 是否存在
if not exist ".venv" (
    echo 创建虚拟环境 .venv...
    python -m venv .venv
)

:: 2. 使用根目录的 pip 安装依赖
echo 正在安装/更新 Python 依赖...
:: 注意：这里假设 requirements.txt 在根目录，如果不在，请改为 backend/requirements.txt
.\.venv\Scripts\python.exe -m pip install --upgrade pip
if exist "requirements.txt" (
    .\.venv\Scripts\pip install -r requirements.txt
) else (
    echo [警告] 根目录没找到 requirements.txt，尝试在 backend 下寻找...
    if exist "backend\requirements.txt" (
        .\.venv\Scripts\pip install -r backend\requirements.txt
    )
)

echo.
echo ==========================================
echo       [2/3] 构建前端 (进入 sam-newton)...
echo ==========================================

:: 🔥 关键修改：进入 frontend/sam-newton 目录
cd frontend\sam-newton

:: 3. 安装前端依赖
if not exist "node_modules" (
    echo 安装 npm 依赖...
    call npm install
)

:: 4. 再次检查 package.json 是否有 build 脚本
findstr /C:"\"build\"" package.json >nul
if %errorlevel% neq 0 (
    echo.
    echo [严重错误] frontend\sam-newton\package.json 里还是没有 "build" 脚本！
    echo 请打开该文件，确保 "scripts" 里包含: "build": "vite build"
    pause
    exit /b
)

:: 5. 构建
echo 开始构建 (npm run build)...
call npm run build

:: 回到根目录
cd ..\..

echo.
echo ==========================================
echo       [3/3] 启动服务 (PM2)...
echo ==========================================

:: 6. 启动 PM2
call pm2 start ecosystem.config.js --update-env

:: 保存进程列表
call pm2 save

echo.
echo [成功] 服务已启动!
echo -------------------------------------
echo 前端访问: http://localhost:8080
echo 后端接口: http://localhost:5000
echo -------------------------------------
pause