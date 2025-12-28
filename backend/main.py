from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.newton.router import router as newton_router
from apps.newton.moments_router import router as moments_router
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI()

# 1. 配置跨域 (解决前端请求报错)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境请改为前端具体地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 挂载路由 (关键点！)
# 我们将路由挂载到 /api/newton，这样接口地址就是 /api/newton/register
app.include_router(newton_router, prefix="/api/newton", tags=["Newton"])
app.include_router(moments_router, prefix="/api/newton", tags=["NewtonMoments"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Newton System Online"}

if __name__ == "__main__":
    import uvicorn
    # 启动服务
    uvicorn.run(app, host="0.0.0.0", port=5000)
