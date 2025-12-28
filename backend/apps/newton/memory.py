import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

MEMOS_API_KEY = os.getenv("MEMOS_API_KEY")
MEMOS_BASE_URL = "https://memos.memtensor.cn/api/openmem/v1"

def _get_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Token {MEMOS_API_KEY}"
    }

async def search_memories(query: str, user_id: str, conv_id: str) -> str:
    """对应文档 4: Retrieve Related Memories"""
    if not MEMOS_API_KEY or not query: return ""
    
    url = f"{MEMOS_BASE_URL}/search/memory"
    payload = {"query": query, "user_id": str(user_id), "conversation_id": conv_id}

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(url, headers=_get_headers(), json=payload, timeout=5.0)
            if res.status_code != 200: return ""
            
            data = res.json()
            # 兼容 soul_mate 项目的字段提取逻辑
            mem_list = data.get("memory_detail_list") or data.get("data", {}).get("memories") or []
            
            summary = []
            # 过滤高置信度记忆
            valid_mems = [m['memory_value'] for m in mem_list if m.get('confidence', 0) > 0.7]
            if valid_mems:
                summary.append("【回忆 & 相关背景】:")
                summary.extend([f"- {m}" for m in valid_mems[:5]])
                
            return "\n".join(summary)
    except Exception as e:
        logger.error(f"⚠️ MemOS Search Error: {e}")
        return ""

async def save_memory(messages: list, user_id: str, conv_id: str):
    """对应文档 3: Store Raw Conversations"""
    if not MEMOS_API_KEY: return
    
    url = f"{MEMOS_BASE_URL}/add/message"
    payload = {"user_id": str(user_id), "conversation_id": conv_id, "messages": messages}

    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, headers=_get_headers(), json=payload, timeout=5.0)
            logger.info("✅ MemOS Memory synced")
    except Exception as e:
        logger.error(f"❌ MemOS Sync Error: {e}")