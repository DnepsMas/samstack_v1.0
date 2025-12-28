from pydantic import BaseModel
from typing import Optional

class AuthRequest(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    userId: str  # 对应数据库中的 username
    message: str
    conversationId: str = "conv_newton"

class GreetRequest(BaseModel):
    userId: str
    conversationId: str = "conv_newton"

class HistoryRequest(BaseModel):
    userId: str
    conversationId: str = "conv_newton"