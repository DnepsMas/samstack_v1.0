<template>
  <div class="app-container">
    
    <div v-if="!currentUser" class="login-layer">
      <div class="login-card">
        <div class="scan-fx"></div>
        <h1 class="sys-title">NEWTON<span class="highlight">.SYS</span></h1>
        <p class="sys-sub">IDENTITY VERIFICATION REQUIRED</p>
        
        <div class="form-group">
          <input v-model="loginForm.username" type="text" class="sys-input" placeholder="ACCESS ID" @keyup.enter="handleAuth('login')">
        </div>
        <div class="form-group">
          <input v-model="loginForm.password" type="password" class="sys-input" placeholder="PASSCODE" @keyup.enter="handleAuth('login')">
        </div>

        <div class="action-group">
          <button @click="handleAuth('login')" class="sys-btn main">LOGIN</button>
          <button @click="handleAuth('register')" class="sys-btn sub">REGISTER</button>
        </div>
        <p v-if="authMsg" class="sys-err">>> {{ authMsg }}</p>
      </div>
    </div>

    <div v-else class="chat-layer">
      
      <header class="header">
        <div class="header-left">
          <div class="avatar-wrapper">
            <img :src="currentPersonaId === 'conv_newton' ? newtonImg : leibnizImg" class="header-avatar">
            <div class="online-dot"></div>
          </div>
          <div class="info-wrapper">
            <select v-model="currentPersonaId" @change="switchPersona" class="persona-switcher">
              <option value="conv_newton">Isaac Newton</option>
              <option value="conv_leibniz">G.W. Leibniz</option>
            </select>
            <span class="status-tag">Connected to MemOS</span>
          </div>
        </div>
        
        <div class="header-right">
          <button @click="goToMoments" class="icon-btn-top moments-btn" title="Chronicle">
            <i class="fas fa-camera-retro"></i>
          </button>
          <button @click="DoTest" class="icon-btn-top Dotest-btn" title="Chronicle">
            <i class="fas fa-chain"></i>
          </button>
          <button @click="logout" class="icon-btn-top power-btn" title="Disconnect">
            <i class="fas fa-power-off"></i>
          </button>
        </div>
      </header>

      <main class="chat-viewport" ref="chatBoxRef" :class="{ 'kb-active': isKbOpen }">
        <div class="message-list">
          <div v-for="(msg, index) in messages" :key="index" :class="['row', msg.role === 'user' ? 'row-user' : 'row-ai']">
            
            <div v-if="msg.role !== 'user'" class="avatar-col">
              <img :src="getAvatarUrl(msg.role)" class="msg-avatar" @error="onImgError">
            </div>

            <div class="content-col">
              <div v-if="msg.role !== 'user'" class="sender-name">
                {{ currentPersonaId === 'conv_newton' ? 'Newton' : 'Leibniz' }}
              </div>
              
              <div class="bubble">
                <div v-if="msg.loading" class="typing">
                  <span>●</span><span>●</span><span>●</span>
                </div>
                <div v-else class="markdown-body" v-html="msg.html || smartRender(msg.content)"></div>
              </div>
            </div>

          </div>
        </div>
      </main>

      

      <footer class="input-dock" :class="{ 'dock-open': isKbOpen }">
        <div class="dock-bar">
          <button class="icon-btn" @click="toggleKeyboard" :class="{ 'active': isKbOpen }">
            <i :class="isKbOpen ? 'fas fa-keyboard' : 'fas fa-plus'"></i>
          </button>
          
          <div class="input-box">
            <textarea 
              ref="inputRef"
              v-model="inputText"
              placeholder="Type message..."
              rows="1"
              @input="autoResize"
              @keydown.enter.exact.prevent="sendMessage"
            ></textarea>
          </div>

          <button class="send-btn" @click="sendMessage" :disabled="!inputText.trim()">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>

        <div v-show="isKbOpen" class="keyboard-area">
          <div class="kb-tabs">
            <div v-for="tab in ['main', 'func', 'sym', 'abc']" :key="tab" 
                 :class="['kb-tab', activeTab === tab ? 'active' : '']"
                 @click="activeTab = tab">
              {{ tab.toUpperCase() }}
            </div>
          </div>
          
          <div class="kb-content">
             <div v-show="activeTab === 'main'" class="kb-grid main-grid">
                <div class="key italic" @click="ins('x')">x</div>
                <div class="key italic" @click="ins('y')">y</div>
                <div class="key" @click="ins('^2')">x²</div>
                <div class="key" @click="ins('\\frac{}{}')">÷</div>
                <div class="key num" @click="ins('7')">7</div>
                <div class="key num" @click="ins('8')">8</div>
                <div class="key num" @click="ins('9')">9</div>
                <div class="key act del" @click="cmd('backspace')">⌫</div>

                <div class="key" @click="ins('(')">(</div>
                <div class="key" @click="ins(')')">)</div>
                <div class="key" @click="ins('\\sqrt{}')">√</div>
                <div class="key" @click="ins('\\int')">∫</div>
                <div class="key num" @click="ins('4')">4</div>
                <div class="key num" @click="ins('5')">5</div>
                <div class="key num" @click="ins('6')">6</div>
                <div class="key" @click="ins('\\times')">×</div>

                <div class="key" @click="ins('\\pi')">π</div>
                <div class="key" @click="ins('e')">e</div>
                <div class="key" @click="ins('^')">^</div>
                <div class="key" @click="ins('_')">_</div>
                <div class="key num" @click="ins('1')">1</div>
                <div class="key num" @click="ins('2')">2</div>
                <div class="key num" @click="ins('3')">3</div>
                <div class="key" @click="ins('-')">-</div>

                <div class="key small" @click="activeTab='func'">ƒ(x)</div>
                <div class="key small" @click="activeTab='sym'">αβ</div>
                <div class="key" @click="ins('.')">.</div>
                <div class="key" @click="ins('=')">=</div>
                <div class="key num wide" @click="ins('0')">0</div>
                <div class="key act enter" @click="sendMessage">ENTER</div>
             </div>

             <div v-show="activeTab === 'abc'" class="kb-col">
                <div class="kb-row"><div v-for="k in 'qwertyuiop'" :key="k" class="key" @click="ins(k)">{{k}}</div></div>
                <div class="kb-row pad"><div v-for="k in 'asdfghjkl'" :key="k" class="key" @click="ins(k)">{{k}}</div></div>
                <div class="kb-row">
                   <div class="key act" @click="activeTab='main'">123</div>
                   <div v-for="k in 'zxcvbnm'" :key="k" class="key" @click="ins(k)">{{k}}</div>
                   <div class="key act del" @click="cmd('backspace')">⌫</div>
                </div>
                <div class="kb-row"><div class="key space" @click="ins(' ')">SPACE</div><div class="key act enter" @click="sendMessage">SEND</div></div>
             </div>

             <div v-show="activeTab === 'func'" class="kb-grid func-grid">
                 <div v-for="f in ['\\sin','\\cos','\\tan','\\log','\\ln','\\lim','\\sum','\\prod','\\int','\\partial','\\nabla']" 
                      :key="f" class="key" @click="ins(f)">{{ f.replace('\\','') }}</div>
                 <div class="key act" @click="activeTab='main'">BACK</div>
             </div>

             <div v-show="activeTab === 'sym'" class="kb-grid sym-grid">
                 <div v-for="s in ['\\alpha','\\beta','\\gamma','\\theta','\\lambda','\\pi','\\infty','\\neq','\\approx']" 
                      :key="s" class="key" @click="ins(s)">{{ s.replace('\\','') }}</div>
                 <div class="key act" @click="activeTab='main'">BACK</div>
             </div>
          </div>
        </div>
      </footer>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router' // 引入 router
import axios from 'axios'
import MarkdownIt from 'markdown-it'
import texmath from 'markdown-it-texmath'
import katex from 'katex'
import 'katex/dist/katex.min.css'

// 1. 本地图片
import newtonImg from '../assets/newton.png'
import leibnizImg from '../assets/leibniz.png'

const router = useRouter() // 初始化 router

// 2. 初始化引擎
const md = new MarkdownIt({ html: true, breaks: true })
    .use(texmath, { engine: katex, delimiters: 'dollars', katexOptions: { throwOnError: false } });

// 3. 状态管理
const API_BASE = 'http://localhost:5000/api/newton'
const storedId = localStorage.getItem('userId')
const currentUser = ref((storedId && storedId !== 'null' && storedId !== 'undefined') ? storedId : null)
const currentPersonaId = ref('conv_newton')
const loginForm = reactive({ username: '', password: '' })
const authMsg = ref('')
const messages = ref([])
const inputText = ref('')
const isKbOpen = ref(false)
const activeTab = ref('main')
const chatBoxRef = ref(null)
const inputRef = ref(null)

// 4. 智能渲染 (保留所有清洗逻辑)
const smartRender = (text) => {
    if (!text) return ''
    let processed = text
        .replace(/\\cdotp/g, '\\cdot')
        .replace(/\\ /g, ' ')
        .replace(/\\text\{([^{}]+)\}/g, '$1')
        .replace(/\\\[/g, '$$').replace(/\\\]/g, '$$')
        .replace(/\\\(/g, '$').replace(/\\\)/g, '$')
    
    return md.render(processed)
}
const previewHtml = computed(() => smartRender(inputText.value))

// 5. 业务逻辑
const getAvatarUrl = (role) => {
    return currentPersonaId.value === 'conv_newton' ? newtonImg : leibnizImg
}
const onImgError = (e) => { e.target.src = 'https://placehold.co/100x100/333/fff?text=IMG' }

// 跳转逻辑
const goToMoments = () => {
    router.push('/newton/moments')
}
const DoTest = () => {
    router.push('/newton/test')
}
const autoResize = () => {
    const el = inputRef.value; if(!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 120) + 'px'
}

const scrollToBottom = () => nextTick(() => {
    if (chatBoxRef.value) chatBoxRef.value.scrollTop = chatBoxRef.value.scrollHeight
})

const triggerGreeting = async () => {
    const loadingMsg = reactive({ role: 'ai', content: '', html: '', loading: true })
    messages.value.push(loadingMsg)
    scrollToBottom()

    try {
        const res = await axios.post(`${API_BASE}/greet`, { 
            userId: currentUser.value, 
            conversationId: currentPersonaId.value 
        })
        if (res.data.success) {
            loadingMsg.loading = false
            loadingMsg.content = res.data.greeting
            loadingMsg.html = smartRender(res.data.greeting)
            scrollToBottom()
        } else {
            messages.value.pop()
        }
    } catch(e) {
        messages.value.pop()
    }
}

const handleAuth = async (type) => {
    const username = loginForm.username.trim()
    const password = loginForm.password.trim()
    if (!username || !password) {
        authMsg.value = "账号和密码不能为空"
        return
    }
    try {
        const res = await axios.post(`${API_BASE}/${type === 'register'?'register':'login'}`, {
            username,
            password,
        })
        if (res.data.success) {
            if (type === 'login') {
                const uid = res.data.memosId || res.data.userId
                currentUser.value = uid
                localStorage.setItem('userId', uid)
                messages.value = []
                await loadHistory()
                await triggerGreeting()
            } else authMsg.value = "注册成功!请登录"
        } else authMsg.value = res.data.message
    } catch(e) { authMsg.value = "Connection Error" }
}

const loadHistory = async () => {
    if (!currentUser.value) return
    try {
        const res = await axios.post(`${API_BASE}/history`, { 
            userId: currentUser.value, 
            conversationId: currentPersonaId.value 
        })
        if (res.data.success) {
            messages.value = res.data.history.map(m => ({ 
                ...m, 
                html: smartRender(m.content) 
            }))
            scrollToBottom()
        }
    } catch(e) {}
}

const sendMessage = async () => {
    const text = inputText.value.trim(); if (!text) return
    messages.value.push({ role: 'user', content: text, html: smartRender(text) })
    inputText.value = ''; autoResize(); scrollToBottom()

    const aiMsg = reactive({ role: 'ai', content: '', html: '', loading: true })
    messages.value.push(aiMsg); scrollToBottom()

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                userId: currentUser.value, 
                message: text, 
                conversationId: currentPersonaId.value 
            })
        })
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        aiMsg.loading = false
        
        while (true) {
            const {done, value} = await reader.read()
            if (done) break
            aiMsg.content += decoder.decode(value, {stream: true})
            aiMsg.html = smartRender(aiMsg.content)
            scrollToBottom()
        }
    } catch(e) { 
        aiMsg.loading = false
        aiMsg.html = "服务器开小差啦~" 
    }
}

const logout = () => { currentUser.value = null; localStorage.clear(); messages.value = [] }
const switchPersona = async () => { 
    messages.value = [] 
    await loadHistory()
    await triggerGreeting()
}
const toggleKeyboard = () => { isKbOpen.value = !isKbOpen.value; setTimeout(scrollToBottom, 100) }

const ins = (txt) => {
    const el = inputRef.value; if(!el) return
    const start = el.selectionStart
    inputText.value = inputText.value.slice(0,start) + txt + inputText.value.slice(el.selectionEnd)
    nextTick(() => { el.focus(); el.selectionStart = start + txt.length; autoResize() })
}
const cmd = (act) => {
    const el = inputRef.value; if(!el) return
    if(act==='backspace' && el.selectionStart>0) {
        inputText.value = inputText.value.slice(0, el.selectionStart-1) + inputText.value.slice(el.selectionStart)
        nextTick(() => { el.focus(); el.selectionStart--; autoResize() })
    }
}

onMounted(() => { if(currentUser.value) loadHistory() })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Roboto+Mono:wght@400;500&display=swap');

/* === 全局 === */
.app-container {
    position: fixed; inset: 0;
    font-family: 'Roboto Mono', monospace;
    background: #050505; color: #e0e0e0;
    overflow: hidden;
    background-image: radial-gradient(circle at 50% 50%, #111 0%, #000 100%);
}

/* === 登录层 === */
.login-layer {
    position: absolute; inset: 0; z-index: 1000;
    display: flex; align-items: center; justify-content: center;
    background: #000;
}
.login-card {
    width: 320px; padding: 40px;
    background: rgba(15, 17, 21, 0.95);
    border: 1px solid #333; border-radius: 8px;
    box-shadow: 0 0 40px rgba(0, 243, 255, 0.1);
    text-align: center; position: relative;
}
.scan-fx { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: #00f3ff; opacity: 0.5; animation: scan 3s infinite linear; }
@keyframes scan { 0% { top: 0; } 100% { top: 100%; } }

.sys-title { font-family: 'Orbitron'; font-size: 2rem; color: #fff; margin: 0; letter-spacing: 2px; text-shadow: 2px 0 #ff0055; }
.highlight { color: #00f3ff; }
.sys-sub { font-size: 0.7rem; color: #666; margin: 10px 0 30px; letter-spacing: 1px; }

.input-group { margin-bottom: 15px; }
.sys-input {
    width: 100%; padding: 12px; background: #000; border: 1px solid #333;
    color: #00f3ff; text-align: center; font-family: inherit; font-size: 1rem;
    outline: none; box-sizing: border-box;
}
.sys-input:focus { border-color: #00f3ff; }

.action-group { display: flex; gap: 10px; margin-top: 20px; }
.sys-btn { flex: 1; padding: 12px; cursor: pointer; border: 1px solid #333; background: transparent; color: #888; font-weight: bold; }
.sys-btn.main { flex: 2; border-color: #00f3ff; color: #00f3ff; background: rgba(0,243,255,0.1); }
.sys-btn:hover { background: #00f3ff; color: #000; }
.sys-err { color: #ff0055; font-size: 0.8rem; margin-top: 15px; }

/* === 聊天层 === */
.chat-layer {
    display: flex; flex-direction: column; height: 100%; width: 100%;
}

.header {
    height: 60px; flex-shrink: 0;
    display: flex; justify-content: space-between; align-items: center;
    padding: 0 20px; background: rgba(10,10,10,0.95); border-bottom: 1px solid #222;
    z-index: 50; backdrop-filter: blur(10px);
}
.header-left { display: flex; align-items: center; gap: 12px; }
/* 🔥 Header Right Flex Layout 🔥 */
.header-right { display: flex; align-items: center; gap: 15px; }

.avatar-wrapper { position: relative; width: 40px; height: 40px; }
.header-avatar { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 1px solid #333; }
.online-dot { position: absolute; bottom: 0; right: 0; width: 10px; height: 10px; background: #00ff00; border-radius: 50%; border: 2px solid #000; }
.persona-switcher { background: transparent; border: none; color: #fff; font-family: 'Orbitron'; font-size: 1rem; cursor: pointer; outline: none; }
.persona-switcher option { background: #111; }
.status-tag { font-size: 0.7rem; color: #00f3ff; opacity: 0.7; display: block; }

/* 🔥 Header Icons Style 🔥 */
.icon-btn-top {
    background: transparent; border: none; color: #fff; font-size: 1.2rem;
    cursor: pointer; padding: 5px; transition: all 0.3s;
}
.moments-btn:hover { color: #00f3ff; text-shadow: 0 0 8px #00f3ff; transform: rotate(90deg); }
.power-btn { color: #ff5555; opacity: 0.8; }
.power-btn:hover { color: #ff5555; text-shadow: 0 0 8px #ff5555; opacity: 1; }

.chat-viewport {
    flex: 1; overflow-y: auto; padding-bottom: 20px;
    display: flex; flex-direction: column;
}
.message-list {
    padding: 20px 15px; display: flex; flex-direction: column; gap: 20px;
}

/* 消息行 */
.row { display: flex; width: 100%; gap: 10px; }
.row-ai { justify-content: flex-start; }
.row-user { justify-content: flex-end; } 

.avatar-col { flex-shrink: 0; }
.msg-avatar { width: 38px; height: 38px; border-radius: 6px; object-fit: cover; border: 1px solid #333; }

.content-col { display: flex; flex-direction: column; max-width: 85%; }
.row-user .content-col { align-items: flex-end; }

.sender-name { font-size: 0.7rem; color: #666; margin-bottom: 4px; margin-left: 2px; }

/* 气泡 - 强制换行与颜色 */
.bubble {
    padding: 10px 14px; border-radius: 12px; font-size: 0.95rem; line-height: 1.6;
    word-break: break-word; overflow-wrap: break-word;
    position: relative;
}
.row-ai .bubble {
    background: #1a1a1a; color: #eee;
    border: 1px solid #333; border-left: 3px solid #00f3ff;
    border-top-left-radius: 2px;
}
.row-user .bubble {
    background: #0d3b3b; color: #fff;
    border: 1px solid #00f3ff;
    border-top-right-radius: 2px;
}

/* Loading 动画 */
.typing span { display: inline-block; animation: blink 1.4s infinite; font-size: 1.2rem; color: #00f3ff; margin: 0 2px; }
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }

/* Dock */
.preview-panel {
    position: absolute; bottom: 60px; left: 0; right: 0; z-index: 80;
    background: rgba(0,0,0,0.9); border-top: 1px solid #00f3ff;
    padding: 10px; max-height: 120px; overflow-y: auto;
    backdrop-filter: blur(10px); color: #00f3ff;
}
.input-dock {
    flex-shrink: 0; background: #0f1115; border-top: 1px solid #333;
    padding-bottom: env(safe-area-inset-bottom);
    display: flex; flex-direction: column;
}
.dock-bar {
    display: flex; align-items: flex-end; padding: 10px; gap: 10px; min-height: 50px;
}
.icon-btn {
    width: 36px; height: 36px; border-radius: 50%; border: none; background: transparent; color: #888; font-size: 1.2rem; cursor: pointer; flex-shrink: 0;
}
.icon-btn.active { color: #00f3ff; background: rgba(0,243,255,0.1); }

.input-box {
    flex: 1; background: #222; border-radius: 20px; padding: 8px 15px; border: 1px solid #333; display: flex; align-items: center;
}
textarea {
    width: 100%; background: transparent; border: none; color: #fff;
    font-family: inherit; font-size: 1rem; resize: none; outline: none;
    max-height: 120px; overflow-y: auto; padding: 0; line-height: 1.4;
}
.send-btn {
    width: 40px; height: 40px; border-radius: 50%; border: none; background: #00f3ff; color: #000; font-size: 1rem; cursor: pointer; flex-shrink: 0;
}
.send-btn:disabled { background: #333; color: #666; cursor: not-allowed; }

/* 键盘 */
.keyboard-area { height: 260px; background: #080808; border-top: 1px solid #333; display: flex; flex-direction: column; }
.kb-tabs { display: flex; background: #111; height: 36px; }
.kb-tab { flex: 1; display: flex; align-items: center; justify-content: center; color: #666; cursor: pointer; font-size: 0.8rem; }
.kb-tab.active { color: #00f3ff; background: rgba(0,243,255,0.05); border-bottom: 2px solid #00f3ff; }
.kb-content { flex: 1; overflow-y: auto; padding: 5px; }

.kb-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 3px; }
.main-grid { grid-template-columns: repeat(8, 1fr); }
.func-grid { grid-template-columns: repeat(4, 1fr); grid-auto-rows: 45px; }
.sym-grid { grid-template-columns: repeat(5, 1fr); grid-auto-rows: 45px; }
.kb-col { display: flex; flex-direction: column; gap: 5px; }
.kb-row { display: flex; gap: 3px; justify-content: center; }
.kb-row.pad { padding: 0 10px; }

.key {
    background: #1e1e1e; color: #ddd; border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; user-select: none; font-size: 1rem; padding: 10px 0;
    box-shadow: 0 2px 0 #000;
}
.key:active { transform: translateY(2px); background: #00f3ff; color: #000; box-shadow: none; }
.key.num { background: #2a2a2a; color: #fff; }
.key.act { background: #333; font-size: 0.8rem; }
.key.del { color: #ff5555; }
.key.enter { background: #00f3ff; color: #000; grid-column: span 2; }
.key.wide { grid-column: span 2; }
.key.small { font-size: 0.8rem; }
.kb-row .key { flex: 1; }
.kb-row .space { flex: 4; }

:deep(.katex-display) { overflow-x: auto; overflow-y: hidden; max-width: 100%; margin: 0.5em 0; }
</style>
