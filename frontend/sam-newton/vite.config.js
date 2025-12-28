// frontend/sam-newton/vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8000,      // 🔥 前端跑在 8000
    host: '0.0.0.0', // 允许局域网访问
    strictPort: true, // 如果 8000 被占用直接报错，不自动换端口
  }
})