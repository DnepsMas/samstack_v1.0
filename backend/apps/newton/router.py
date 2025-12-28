from fastapi import APIRouter, HTTPException
import hashlib
import sqlite3
import asyncio
from . import crud, services, memory
from .schemas import ChatRequest, AuthRequest, GreetRequest, HistoryRequest
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/register")
async def register(req: AuthRequest):
    """
    用户注册：创建本地账号并映射 MemOS 身份
    """
    try:
        # 1. 检查用户是否已存在
        if crud.get_user(req.username):
            return {"success": False, "message": "用户名已存在"}
        
        # 2. 密码加盐哈希处理
        pwd_hash = hashlib.sha256(req.password.encode()).hexdigest()
        
        # 3. 这里的 memos_uid 必须在后续 chat 中作为 user_id 传给 MemOS API
        memos_uid = f"user_{req.username}"
        
        # 4. 写入数据库
        conn = sqlite3.connect(crud.DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password_hash, memos_user_id, current_conv_id) VALUES (?, ?, ?, ?)", 
                  (req.username, pwd_hash, memos_uid, "conv_newton"))
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "注册成功", "memosId": memos_uid}
    except Exception as e:
        return {"success": False, "message": f"注册失败: {str(e)}"}

@router.post("/login")
async def login(req: AuthRequest):
    """
    用户登录：验证身份并返回对应的 MemOS ID
    """
    pwd_hash = hashlib.sha256(req.password.encode()).hexdigest()
    user = crud.get_user(req.username)
    if user and user[1] == pwd_hash:
        return {
            "success": True, 
            "userId": user[0], 
            "memosId": user[2] # 返回给前端，后续请求带上此 ID
        }
    return {"success": False, "message": "用户名或密码错误或用户不存在"}

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # 步骤 1：获取 MemOS 上下文
    memory_ctx = await memory.search_memories(req.message, req.userId, req.conversationId)

    # 步骤 2：调用 AI 流式生成
    openai_stream = await services.chat_with_persona(req.userId, req.message, memory_ctx, req.conversationId)

    async def response_generator():
        full_text = ""
        async for chunk in openai_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_text += content
                yield content
        
        # 步骤 3：存入本地 DB 并异步同步至 MemOS
        if full_text:
            crud.save_message(req.userId, req.conversationId, "user", req.message)
            crud.save_message(req.userId, req.conversationId, "ai", full_text)
            
            memos_msgs = [{"role": "user", "content": req.message}, {"role": "assistant", "content": full_text}]
            asyncio.create_task(memory.save_memory(memos_msgs, req.userId, req.conversationId))

    return StreamingResponse(response_generator(), media_type="text/plain")

@router.post("/history")
async def get_history(req: HistoryRequest):
    return {"success": True, "history": crud.get_history(req.userId, req.conversationId)}

@router.post("/greet")
async def greet(req: GreetRequest):
    ctx = await memory.search_memories("用户上线", req.userId, req.conversationId)
    msg = await services.generate_greeting(req.userId, req.conversationId, ctx)
    return {"success": True, "greeting": msg}
