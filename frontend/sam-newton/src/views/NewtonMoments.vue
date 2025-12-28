<template>
  <div class="moments-app">
    <header class="nav-header">
      <div class="nav-left" @click="goBack">
        <i class="fas fa-chevron-left"></i> <span>BACK</span>
      </div>
      <div class="nav-title">CHRONICLE</div>
      <div class="nav-right"></div>
    </header>

    <main class="scroll-container">
      <div class="cover-area">
        <div class="cover-img"></div>
        <div class="user-profile">
          <div class="profile-text">
            <h2 class="p-name">{{ userId }}</h2>
            <p class="p-sign">Nature and Nature's laws lay hid in night.</p>
          </div>
          <div class="p-avatar-box">
            <div class="p-avatar placeholder"></div>
          </div>
        </div>
      </div>

      <div class="feed-list">
        <div v-if="loading" class="feed-status">Loading...</div>
        <div v-else-if="error" class="feed-status error">{{ error }}</div>
        <template v-else>
          <div
            v-for="(item, idx) in displayMoments"
            :key="item.id"
            class="feed-item"
            :class="{ 'border-top': idx > 0 }"
          >
            <div class="feed-left">
              <img :src="avatarFor(item)" class="feed-avatar">
            </div>
            <div class="feed-right">
              <div class="feed-name">{{ item.author_name }}</div>
              <div class="feed-content" v-html="contentHtml(item)"></div>
              <div v-if="item.media && item.media.length" class="feed-images">
                <div v-for="(m, mi) in item.media" :key="mi" class="f-img-box" :class="{ 'is-image': isImage(m) }">
                  <img v-if="isImage(m)" :src="m" class="f-img-img">
                  <span v-else>{{ m }}</span>
                </div>
              </div>
              <div class="feed-footer">
                <span class="feed-time">{{ formatTime(item.created_at) }}</span>
                <div class="feed-action">
                  <i class="far fa-heart"></i>
                  <i class="far fa-comment"></i>
                </div>
              </div>
              <div v-if="item.comments && item.comments.length" class="feed-comments">
                <div v-for="c in item.comments" :key="c.id" class="comment-row">
                  <span class="c-user">{{ c.author_name }}:</span> <span class="c-text">{{ c.content_text }}</span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import MarkdownIt from 'markdown-it'
import texmath from 'markdown-it-texmath'
import katex from 'katex'
import 'katex/dist/katex.min.css'

// 导入图片 (路径请根据你实际项目调整)
import newtonImg from '../assets/newton.png'
import leibnizImg from '../assets/leibniz.png'

const router = useRouter()
const userId = ref('Unknown')
const moments = ref([])
const loading = ref(false)
const error = ref('')
const sampleMoments = [
    {
        id: 'sample-1',
        author_name: 'Isaac Newton',
        author_avatar_url: newtonImg,
        content_markdown: '刚刚在这个苹果树下悟出了一些道理。万物皆有引力，且与距离平方成反比。\n\n$$ F = G \\\\frac{m_1 m_2}{r^2} $$',
        content_html: null,
        media: ['🍎'],
        created_at: '1 hour ago',
        comments: [],
    },
    {
        id: 'sample-2',
        author_name: 'G.W. Leibniz',
        author_avatar_url: leibnizImg,
        content_markdown: '这种符号 $$\\\\int f(x) dx$$ 显然比流数术优美多了，某些人不要太固执。Analysis is about elegance.',
        content_html: null,
        media: null,
        created_at: 'Yesterday',
        comments: [
            {
                id: 'sample-2-c1',
                author_name: 'Newton',
                content_text: '你那是抄袭！Plagiarism!',
            },
        ],
    },
]
const displayMoments = computed(() => [...sampleMoments, ...moments.value])

// 初始化渲染引擎 (保持公式渲染能力)
const md = new MarkdownIt({ html: true, breaks: true })
    .use(texmath, { engine: katex, delimiters: 'dollars', katexOptions: { throwOnError: false } });

// 渲染函数
const smartRender = (text) => {
    if (!text) return ''
    let processed = text
        .replace(/\\cdotp/g, '\\cdot')
        .replace(/\\text\{([^{}]+)\}/g, '$1') // 去壳
        .replace(/\$\s*[\r\n]+([\s\S]*?)[\r\n]+\s*\$/g, '$$$1$$') // 修复换行公式
    return md.render(processed)
}

const contentHtml = (item) => {
    if (!item) return ''
    if (item.content_html) return item.content_html
    return smartRender(item.content_markdown || '')
}

const isImage = (value) => {
    if (!value) return false
    return typeof value === 'string' && (value.startsWith('http') || value.startsWith('/'))
}

const formatTime = (value) => {
    if (!value) return ''
    const dt = new Date(value)
    if (Number.isNaN(dt.getTime())) return value
    const now = new Date()
    const diffMs = now.getTime() - dt.getTime()
    const hourMs = 60 * 60 * 1000
    const dayMs = 24 * hourMs
    if (diffMs < dayMs) {
        const hours = Math.max(1, Math.floor(diffMs / hourMs))
        return `${hours}小时前`
    }
    if (diffMs < 3 * dayMs) {
        const days = Math.max(1, Math.floor(diffMs / dayMs))
        return `${days}天前`
    }
    const y = dt.getFullYear()
    const m = String(dt.getMonth() + 1).padStart(2, '0')
    const d = String(dt.getDate()).padStart(2, '0')
    return `${y}-${m}-${d}`
}

const avatarFor = (item) => {
    if (item && item.author_avatar_url) return item.author_avatar_url
    const name = (item && item.author_name) || ''
    if (/leibniz/i.test(name) || name.includes('莱布尼兹')) return leibnizImg
    return newtonImg
}

const refreshUserId = () => {
    const storedId = localStorage.getItem('userId')
    const raw = (storedId && storedId !== 'null' && storedId !== 'undefined') ? storedId : ''
    userId.value = raw.startsWith('user_') ? raw.slice(5) : (raw || 'Unknown')
}

const fetchMoments = async () => {
    loading.value = true
    error.value = ''
    try {
        const res = await fetch('http://127.0.0.1:5000/api/newton/moments?limit=20&offset=0')
        const data = await res.json()
        if (data && data.success) {
            moments.value = data.moments || []
        } else {
            error.value = (data && data.message) || 'Failed to load moments'
        }
    } catch (err) {
        error.value = err?.message || 'Failed to load moments'
    } finally {
        loading.value = false
    }
}

const goBack = () => {
    router.push('/newton') // 假设聊天页是首页，或者 router.go(-1)
}

const handleStorage = (e) => {
    if (e.key === 'userId') refreshUserId()
}

const handleFocus = () => refreshUserId()
const handleVisibility = () => {
    if (document.visibilityState === 'visible') refreshUserId()
}

onMounted(() => {
    refreshUserId()
    fetchMoments()
    window.addEventListener('storage', handleStorage)
    window.addEventListener('focus', handleFocus)
    document.addEventListener('visibilitychange', handleVisibility)
})

onBeforeUnmount(() => {
    window.removeEventListener('storage', handleStorage)
    window.removeEventListener('focus', handleFocus)
    document.removeEventListener('visibilitychange', handleVisibility)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Roboto+Mono:wght@400;500&display=swap');

.moments-app {
    position: fixed; inset: 0;
    background: #050505; color: #e0e0e0;
    font-family: 'Roboto Mono', monospace;
    display: flex; flex-direction: column;
}

/* 顶部导航 */
.nav-header {
    height: 60px; padding: 0 15px;
    display: flex; align-items: center; justify-content: space-between;
    background: rgba(5, 5, 5, 0.8); backdrop-filter: blur(10px);
    position: absolute; top: 0; left: 0; right: 0; z-index: 100;
}
.nav-left { cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 1rem; color: #fff; }
.nav-left:hover { color: #00f3ff; }
.nav-title { font-family: 'Orbitron'; font-weight: bold; letter-spacing: 2px; }

/* 滚动主容器 */
.scroll-container { flex: 1; overflow-y: auto; background: #000; }

/* 封面区域 */
.cover-area { position: relative; margin-bottom: 60px; }
.cover-img {
    height: 300px; width: 100%;
    background: linear-gradient(to bottom, transparent, #000), 
                url('../assets/bg.jpg') center/cover;
}
.user-profile {
    position: absolute; bottom: -40px; right: 20px;
    display: flex; align-items: flex-end; gap: 20px;
}
.profile-text { text-align: right; padding-bottom: 50px; text-shadow: 0 2px 4px #000; }
.p-name { margin: 0; font-family: 'Orbitron'; color: #fff; font-size: 1.4rem; }
.p-sign { margin: 5px 0 0; color: #bbb; font-size: 0.8rem; }
.p-avatar-box {
    width: 80px; height: 80px; border-radius: 12px;
    background: #000; border: 2px solid #333;
    overflow: hidden; flex-shrink: 0;
}
.p-avatar { width: 100%; height: 100%; object-fit: cover; }
.p-avatar.placeholder {
    background: linear-gradient(135deg, #222, #111);
    border: 1px solid #333;
}

/* 动态列表 */
.feed-list { padding: 0 0 40px 0; }
.feed-status { padding: 20px 15px; color: #777; }
.feed-status.error { color: #ff6b6b; }
.feed-item { display: flex; gap: 15px; padding: 25px 15px; }
.feed-item.border-top { border-top: 1px solid #1a1a1a; }

.feed-left { flex-shrink: 0; }
.feed-avatar { width: 45px; height: 45px; border-radius: 6px; object-fit: cover; border: 1px solid #333; }

.feed-right { flex: 1; min-width: 0; }
.feed-name { color: #00f3ff; font-weight: bold; margin-bottom: 6px; font-family: 'Orbitron'; font-size: 0.95rem; }
.feed-content { color: #ddd; font-size: 0.95rem; line-height: 1.6; word-wrap: break-word; }

.feed-images { display: flex; gap: 5px; margin-top: 10px; }
.f-img-box { width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 2rem; border: 1px solid #333; overflow: hidden; }
.f-img-box.is-image { background: #111; }
.f-img-img { width: 100%; height: 100%; object-fit: cover; display: block; }

.feed-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; }
.feed-time { color: #666; font-size: 0.8rem; }
.feed-action { display: flex; gap: 20px; color: #00f3ff; font-size: 1.1rem; cursor: pointer; }

.feed-comments { background: #111; margin-top: 10px; padding: 8px; border-radius: 4px; }
.comment-row { font-size: 0.85rem; line-height: 1.4; }
.c-user { color: #00f3ff; font-weight: bold; margin-right: 5px; }
.c-text { color: #aaa; }

/* 公式修复 */
:deep(.katex-display) { overflow-x: auto; overflow-y: hidden; max-width: 100%; margin: 0.5em 0; }
</style>
