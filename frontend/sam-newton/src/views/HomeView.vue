<script setup>
import { useRouter } from 'vue-router'

// 1. 获取路由实例
const router = useRouter()

// 2. 定义跳转函数 (可选，也可以直接在模板写 router.push)
const navigateTo = (path) => {
  router.push(path)
}
</script>

<template>
  <div class="portal-container">
    <h1 class="portal-title">SAM STACK</h1>
    <div class="card-grid">
      
      <div class="app-card" @click="router.push('/newton')">
        <div class="icon">🍎</div>
        <div class="text-content">
          <h2>Cyber Newton</h2>
          <p>基于 MemOS 的长记忆 AI 导师</p>
        </div>
      </div>

      <div class="app-card" @click="router.push('/pomodoro')">
        <div class="icon">🍅</div>
        <div class="text-content">
          <h2>番茄钟</h2>
          <p>激励智能多功能番茄钟</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* === 容器基础样式 === */
.portal-container {
  min-height: 100vh;
  width: 100%;
  background: #050505;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', sans-serif;
  padding: 20px;
  box-sizing: border-box;
}

.portal-title {
  font-size: 3rem;
  margin-bottom: 3rem;
  text-shadow: 0 0 10px #00f3ff;
  text-align: center;
  line-height: 1.2;
}

/* === 卡片网格 === */
.card-grid {
  display: flex;
  flex-direction: row;
  gap: 30px;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
  max-width: 800px;
}

/* === 卡片样式 === */
.app-card {
  width: 200px; 
  height: 250px;
  background: #0f1115;
  border: 1px solid #333;
  border-radius: 16px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* 增加 text-content 包裹层，为了方便手机端 flex 布局 */
.text-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 悬停特效 */
@media (hover: hover) {
  .app-card:hover {
    border-color: #00f3ff;
    box-shadow: 0 0 25px rgba(0, 243, 255, 0.3);
    transform: translateY(-8px);
    background: #16181d;
  }
}

.icon { 
  font-size: 3.5rem; 
  margin-bottom: 15px; 
  transition: transform 0.3s;
}

.app-card h2 {
  font-size: 1.2rem;
  margin: 0 0 10px 0;
  color: #fff;
}

.app-card p {
  font-size: 0.8rem;
  color: #888;
  margin: 0;
  line-height: 1.4;
}

.disabled { 
  opacity: 0.5; 
  cursor: not-allowed; 
  filter: grayscale(100%);
}

/* === 📱 手机端适配 === */
@media (max-width: 768px) {
  .portal-title {
    font-size: 2.2rem;
    margin-bottom: 2rem;
  }

  .card-grid {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .app-card {
    width: 100%;
    max-width: 320px;
    height: auto;
    aspect-ratio: 16/9; /* 宽屏卡片 */
    flex-direction: row; /* 横向排列 */
    padding: 20px 30px;
    justify-content: flex-start; /* 靠左对齐 */
    text-align: left;
  }

  /* 手机端内部布局调整 */
  .app-card .icon {
    margin-bottom: 0;
    margin-right: 20px;
    font-size: 2.5rem;
  }

  .app-card .text-content {
    align-items: flex-start; /* 文字靠左 */
  }

  .app-card:active {
    background: #1a1c23;
    transform: scale(0.98);
  }
}
</style>