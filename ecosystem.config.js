module.exports = {
    apps: [
        {
            name: "newton-backend",
            // 假设入口文件 main.py 在 backend 文件夹里
            script: "main.py",
            cwd: "./backend",
            // 🔥 关键修改：指向根目录下的 .venv
            interpreter: "../.venv/Scripts/python.exe",
            env: {
                PYTHONIOENCODING: "utf-8"
            }
        },
        {
            name: "newton-frontend",
            script: "serve",
            env: {
                // 🔥 关键修改：指向 sam-newton 下的 dist
                PM2_SERVE_PATH: "./frontend/sam-newton/dist",
                PM2_SERVE_PORT: 8080,
                PM2_SERVE_SPA: "true",
                PM2_SERVE_HOMEPAGE: "/index.html"
            }
        }
    ]
};