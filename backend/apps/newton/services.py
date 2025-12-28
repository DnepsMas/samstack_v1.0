import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from . import crud

# 🔥 核心修复：先加载环境变量，再初始化客户端
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

# 增加防御性判断，防止报错让整个后端起不来
if not api_key:
    print("⚠️ 警告: 未检测到 OPENAI_API_KEY，AI 功能将不可用。")
    # 给一个假 key 防止报错，真正调用时再由 OpenAI 抛错，避免启动崩溃
    client = AsyncOpenAI(api_key="sk-placeholder", base_url=base_url)
else:
    client = AsyncOpenAI(api_key=api_key, base_url=base_url)

PERSONAS = {
    "conv_newton": "身份：艾萨克·牛顿爵士。\n性格:傲慢、严谨。坚信微积分是你发明的。\n要求:输出公式,使用latex符号,仅说中文。",
    "conv_leibniz": "身份：莱布尼兹。\n性格:博学、优雅。喜欢谈论符号逻辑。\n要求:输出公式,使用latex符号,仅说中文。"
}

async def chat_with_persona(user_id: str, message: str, memory_context: str, conv_id: str):
    # 再次检查 key，避免调用时报错
    if client.api_key == "sk-placeholder":
        raise ValueError("OpenAI API Key 未配置")

    base_persona = PERSONAS.get(conv_id, PERSONAS["conv_newton"])
    
    # 注入记忆上下文
    system_prompt = f"你现在完全沉浸在以下身份中：\n{base_persona}\n\n{memory_context}."
    
    # 获取本地历史
    history = crud.get_history(user_id, conv_id, limit=6)
    
    messages = [{"role": "system", "content": system_prompt}]
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    
    messages.append({"role": "user", "content": message})

    return await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=messages,
        stream=True,
        temperature=0.7
    )

async def generate_greeting(user_id: str, conv_id: str, memory_context: str = ""):
    if client.api_key == "sk-placeholder":
        return "档案馆连接断开 (API Key Missing)"

    persona = PERSONAS.get(conv_id)
    prompt = f"{persona}\n\n用户上线。相关记忆：\n{memory_context}\n请以你的身份对用户写一句简单的见面问候（30字内）。"
    
    res = await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "system", "content": prompt}]
    )
    return res.choices[0].message.content