@echo off
chcp 65001 >nul
echo ==========================================
echo       🚀 正在启动 Sam Stack 全栈环境...
echo ==========================================

:: 1. 启动后端 (新窗口)
:: ⚠️ 注意：假设你的 venv 在 backend/venv 目录下
:: 如果你的虚拟环境叫 .venv，请把下面的 venv 改成 .venv
start "Sam Backend (5000)" cmd /k ".venv\Scripts\activate && python backend/main.py"

:: 2. 等待 2 秒，防止端口冲突或后端未就绪
timeout /t 2 /nobreak >nul

:: 3. 启动前端 (新窗口)
start "Sam Frontend (8000)" cmd /k "cd frontend/sam-newton && npm run dev"

echo.
echo ✅ 服务已启动！
echo 🌍 前端地址: http://localhost:8000
echo 🔌 后端地址: http://localhost:5000
echo.
pause