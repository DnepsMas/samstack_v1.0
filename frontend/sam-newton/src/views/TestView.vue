<template>
  <div class="quiz-container">
    <div class="scan-line"></div>
    
    <transition name="fade" mode="out-in">
      <div v-if="step === 'intro'" class="card intro-card" key="intro">
        <h1 class="glitch-title">MENTOR<span class="highlight">.MATCH</span></h1>
        <p class="subtitle">灵魂共鸣度测试系统 v1.0</p>
        <div class="desc">
          <p>在无尽的数学宇宙中，谁才是你的精神向导？</p>
          <p>是那个在苹果树下凝视引力的 <span class="cyan">独行者</span>？</p>
          <p>还是那个在符号海洋中构建逻辑的 <span class="pink">外交家</span>？</p>
        </div>
        <button class="cyber-btn start-btn" @click="startQuiz">
          <i class="fas fa-microchip"></i> START LINK
        </button>
      </div>

      <div v-else-if="step === 'quiz'" class="card quiz-card" key="quiz">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: ((currentIdx + 1) / questions.length) * 100 + '%' }"></div>
        </div>
        
        <div class="question-header">
          <span class="q-tag">QUERY_0{{ currentIdx + 1 }}</span>
        </div>
        
        <h2 class="question-text">{{ currentQuestion.text }}</h2>
        
        <div class="options-grid">
          <button 
            v-for="(opt, idx) in currentQuestion.options" 
            :key="idx" 
            class="option-btn"
            @click="selectOption(opt.type)"
          >
            <span class="opt-prefix">{{ ['A', 'B'][idx] }}</span>
            {{ opt.text }}
          </button>
        </div>
      </div>

      <div v-else-if="step === 'loading'" class="card loading-card" key="loading">
        <div class="spinner"></div>
        <p class="loading-text">ANALYZING NEURAL PATTERNS...</p>
      </div>

      <div v-else-if="step === 'result'" class="card result-card" key="result">
        <div class="result-header">MATCH FOUND</div>
        
        <div class="avatar-box">
          <img :src="result.img" class="result-avatar">
          <div class="circle-ring"></div>
        </div>

        <h2 class="result-name">{{ result.name }}</h2>
        <div class="sync-rate">
          SYNC RATE: <span class="cyan">{{ result.score }}%</span>
        </div>

        <p class="result-desc" v-html="result.desc"></p>

        <div class="action-row">
          <button class="cyber-btn secondary" @click="resetQuiz">RETRY</button>
          <button class="cyber-btn primary" @click="enterChat">ENTER CHAT</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router' // 如果你想跳转回聊天页

// 图片资源 (请确保路径正确)
import newtonImg from '../assets/newton.png'
import leibnizImg from '../assets/leibniz.png'

const router = useRouter()

// 状态
const step = ref('intro') // intro, quiz, loading, result
const currentIdx = ref(0)
const scores = ref({ newton: 0, leibniz: 0 })

// 题库
const questions = [
  {
    text: "当你面对一个极其复杂的数学问题时，你的第一反应是？",
    options: [
      { text: "思考它的物理意义，想象物体是如何运动变化的 (流数术)", type: 'newton' },
      { text: "思考如何用最优雅、通用的符号来表达这种关系 (符号学)", type: 'leibniz' }
    ]
  },
  {
    text: "关于“时间”和“空间”，你更倾向于哪种观点？",
    options: [
      { text: "它们是绝对的容器，上帝的传感器，即使没有物质也依然存在。", type: 'newton' },
      { text: "它们只是物质之间关系的体现，没有物质就没有时空。", type: 'leibniz' }
    ]
  },
  {
    text: "如果在学术上与人发生争执，你会？",
    options: [
      { text: "利用一切手段捍卫自己的优先权，甚至匿名攻击对方。真理不容玷污。", type: 'newton' },
      { text: "尝试建立某种普遍的和谐体系，或者去修个家谱稍微分心一下。", type: 'leibniz' }
    ]
  },
  {
    text: "你更喜欢哪种工作环境？",
    options: [
      { text: "独自一人在避世的乡间，或者半夜的炼金炉旁，绝对安静。", type: 'newton' },
      { text: "游走于宫廷、图书馆和学者之间，兼职做做律师和外交官。", type: 'leibniz' }
    ]
  }
]

const currentQuestion = computed(() => questions[currentIdx.value])

// 结果计算逻辑
const result = computed(() => {
  const isNewton = scores.value.newton > scores.value.leibniz
  return {
    name: isNewton ? 'ISAAC NEWTON' : 'G.W. LEIBNIZ',
    img: isNewton ? newtonImg : leibnizImg,
    score: Math.floor(Math.random() * 15) + 85, // 随机生成 85-99% 的同步率
    desc: isNewton 
      ? "你的灵魂充满孤傲与深刻。你相信直觉与物理实在，<br>像一位在此岸捡拾贝壳的巨人。<br><b>建议：少研究炼金术，多发论文。</b>"
      : "你的思维充满逻辑与和谐。你追求符号的完美与通用的知识，<br>是天生的理性主义者与博学家。<br><b>建议：把微积分那个积分号写大点。</b>"
  }
})

// 方法
const startQuiz = () => { step.value = 'quiz' }

const selectOption = (type) => {
  scores.value[type]++
  if (currentIdx.value < questions.length - 1) {
    currentIdx.value++
  } else {
    step.value = 'loading'
    setTimeout(() => { step.value = 'result' }, 1500) // 模拟计算耗时
  }
}

const resetQuiz = () => {
  currentIdx.value = 0
  scores.value = { newton: 0, leibniz: 0 }
  step.value = 'intro'
}

const enterChat = () => {
  // 这里跳转回你的主聊天页面
  router.push('/newton') 
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Roboto+Mono:wght@400;500&display=swap');

/* 全局容器 */
.quiz-container {
  position: fixed; inset: 0;
  background: #050505; color: #e0e0e0;
  font-family: 'Roboto Mono', monospace;
  display: flex; align-items: center; justify-content: center;
  background-image: radial-gradient(circle at 50% 50%, #111 0%, #000 100%);
  overflow: hidden;
}

/* 扫描线特效 */
.scan-line {
  position: absolute; top: 0; left: 0; width: 100%; height: 3px;
  background: rgba(0, 243, 255, 0.2);
  animation: scan 4s infinite linear;
  pointer-events: none; z-index: 10;
}
@keyframes scan { 0% { top: -10%; } 100% { top: 110%; } }

/* 通用卡片样式 */
.card {
  width: 90%; max-width: 480px;
  background: rgba(15, 17, 21, 0.95);
  border: 1px solid #333; border-radius: 12px;
  padding: 40px; text-align: center;
  box-shadow: 0 0 50px rgba(0, 243, 255, 0.08);
  position: relative;
}

/* 文本样式 */
.glitch-title { font-family: 'Orbitron'; font-size: 2.5rem; color: #fff; margin: 0 0 10px; letter-spacing: 3px; text-shadow: 2px 0 #ff0055; }
.highlight { color: #00f3ff; }
.subtitle { font-size: 0.8rem; color: #666; margin-bottom: 40px; letter-spacing: 2px; }
.desc { color: #aaa; line-height: 1.8; margin-bottom: 40px; font-size: 0.95rem; }
.cyan { color: #00f3ff; font-weight: bold; }
.pink { color: #ff0055; font-weight: bold; }

/* 按钮 */
.cyber-btn {
  background: transparent; border: 1px solid #00f3ff;
  color: #00f3ff; padding: 15px 40px; font-size: 1.1rem;
  cursor: pointer; font-family: 'Orbitron'; letter-spacing: 2px;
  transition: all 0.3s; clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
}
.cyber-btn:hover { background: #00f3ff; color: #000; box-shadow: 0 0 20px rgba(0, 243, 255, 0.4); }
.start-btn i { margin-right: 8px; }

/* 答题页 */
.progress-bar { width: 100%; height: 4px; background: #222; margin-bottom: 20px; border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: #00f3ff; transition: width 0.3s ease; box-shadow: 0 0 10px #00f3ff; }
.question-header { text-align: left; margin-bottom: 20px; }
.q-tag { background: #111; color: #666; padding: 4px 8px; font-size: 0.7rem; border: 1px solid #333; }
.question-text { font-size: 1.2rem; color: #fff; margin-bottom: 30px; line-height: 1.5; min-height: 3.6em; }

.options-grid { display: flex; flex-direction: column; gap: 15px; }
.option-btn {
  background: #0f1115; border: 1px solid #333; color: #ccc;
  padding: 15px 20px; text-align: left; cursor: pointer;
  display: flex; align-items: center; transition: all 0.2s;
  font-family: inherit; font-size: 0.95rem; border-radius: 4px;
}
.option-btn:hover { border-color: #00f3ff; color: #fff; background: rgba(0, 243, 255, 0.05); }
.opt-prefix { color: #666; font-weight: bold; margin-right: 15px; font-family: 'Orbitron'; }
.option-btn:hover .opt-prefix { color: #00f3ff; }

/* 结果页 */
.result-header { font-family: 'Orbitron'; color: #666; letter-spacing: 4px; margin-bottom: 30px; font-size: 0.8rem; }
.avatar-box {
  width: 120px; height: 120px; margin: 0 auto 20px; position: relative;
  display: flex; align-items: center; justify-content: center;
}
.result-avatar { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 3px solid #fff; z-index: 2; }
.circle-ring {
  position: absolute; width: 140%; height: 140%;
  border: 1px dashed #00f3ff; border-radius: 50%;
  animation: spin 10s infinite linear;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.result-name { font-family: 'Orbitron'; font-size: 1.8rem; color: #fff; margin: 10px 0; text-shadow: 0 0 10px rgba(255,255,255,0.3); }
.sync-rate { font-size: 1rem; color: #888; margin-bottom: 20px; }
.result-desc { color: #ccc; line-height: 1.6; margin-bottom: 40px; font-size: 0.9rem; }

.action-row { display: flex; gap: 15px; justify-content: center; }
.cyber-btn.secondary { border-color: #333; color: #888; }
.cyber-btn.secondary:hover { border-color: #fff; color: #fff; background: transparent; }
.cyber-btn.primary { background: #00f3ff; color: #000; }

/* Loading */
.loading-text { margin-top: 20px; color: #00f3ff; font-family: 'Orbitron'; letter-spacing: 2px; animation: blink 1s infinite; }
.spinner {
  width: 50px; height: 50px; border: 3px solid #222;
  border-top: 3px solid #00f3ff; border-radius: 50%;
  margin: 0 auto; animation: spin 1s infinite linear;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

/* Transition */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.fade-enter-from { opacity: 0; transform: scale(0.95); }
.fade-leave-to { opacity: 0; transform: scale(1.05); }
</style>