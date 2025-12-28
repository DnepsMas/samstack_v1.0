<template>
  <div class="input-wrapper-outer">
    
    <div v-if="mode === 'text' && modelValue" class="latex-preview-bubble">
      <div v-html="renderedLatex"></div>
    </div>

    <div 
      class="cyber-input-wrapper" 
      :class="{ 'focused': isFocused }"
      @click="handleWrapperClick"
    >
      <textarea
        v-if="mode === 'text'"
        ref="nativeInputRef"
        :value="modelValue"
        @input="handleTextInput"
        @keydown.enter="handleEnter"
        @focus="handleFocus"
        @blur="handleBlur"
        class="native-textarea"
        placeholder="输入内容..."
        rows="1"
      ></textarea>

      <math-field
        v-else
        ref="mathInputRef"
        :value="modelValue"
        @input="handleMathInput"
        @focus="handleFocus"
        @blur="handleBlur"
        class="math-field-input"
        virtual-keyboard-mode="onfocus" 
      ></math-field>

      <button 
        class="toggle-mode-btn" 
        @mousedown.prevent 
        @click.stop="toggleMode"
      >
        <span v-if="mode === 'text'" style="font-weight:bold; font-family: serif; font-style: italic;">∑</span>
        <span v-else>Aa</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed } from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import 'mathlive'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue', 'enter', 'focus', 'blur'])

const mode = ref('text') 
const nativeInputRef = ref(null)
const mathInputRef = ref(null)
const isFocused = ref(false)

const renderedLatex = computed(() => {
  try {
    return katex.renderToString(props.modelValue || '', {
      throwOnError: false,
      displayMode: false
    })
  } catch (e) {
    return props.modelValue 
  }
})

const adjustHeight = () => {
  if (nativeInputRef.value) {
    nativeInputRef.value.style.height = 'auto'
    nativeInputRef.value.style.height = nativeInputRef.value.scrollHeight + 'px'
  }
}

const handleTextInput = (e) => {
  emit('update:modelValue', e.target.value)
  adjustHeight()
}

const handleMathInput = (e) => {
  emit('update:modelValue', e.target.value)
}

const handleEnter = (e) => {
  if (!e.shiftKey) {
    e.preventDefault()
    emit('enter')
  }
}

const handleFocus = () => {
  isFocused.value = true
  emit('focus') // 通知父组件调整高度
  setTimeout(() => {
    nativeInputRef.value?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
  }, 300)
}

const handleBlur = () => {
  isFocused.value = false
  emit('blur')
}

// 🔥 核心修改 3：点击外层容器也触发 focus 通知
const handleWrapperClick = () => {
  emit('focus')
  // 帮助聚焦到当前输入框
  if (mode.value === 'text') {
    nativeInputRef.value?.focus()
  } else {
    mathInputRef.value?.focus()
  }
}

const toggleMode = async () => {
  // 🔥 核心修改 4：切换模式瞬间，强制通知父组件“开始算高度！”
  // 哪怕因为切换导致瞬间失焦，这句话也能保证父组件开始 resize 循环
  emit('focus') 

  mode.value = mode.value === 'text' ? 'math' : 'text'
  await nextTick()
  if (mode.value === 'text') {
    nativeInputRef.value?.focus()
    adjustHeight()
  } else {
    mathInputRef.value?.focus()
  }
}

watch(() => props.modelValue, (newVal) => {
  if (!newVal && nativeInputRef.value) {
    nativeInputRef.value.style.height = 'auto'
  }
})
</script>

<style scoped>
.input-wrapper-outer {
  position: relative;
  width: 100%;
}

.latex-preview-bubble {
  position: absolute;
  bottom: 100%;
  left: 0;
  margin-bottom: 8px;
  background: rgba(30, 30, 30, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 12px;
  border-radius: 12px;
  color: #00e676;
  font-size: 14px;
  max-width: 100%;
  pointer-events: none;
  box-shadow: 0 -4px 10px rgba(0,0,0,0.2);
  animation: slideUp 0.2s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.cyber-input-wrapper {
  display: flex;
  align-items: flex-end;
  background: #121212;
  border: 1px solid #333;
  border-radius: 20px;
  padding: 8px 12px;
  width: 100%;
  transition: all 0.3s;
  /* 增加点击区域感知 */
  cursor: text;
}

.cyber-input-wrapper.focused {
  border-color: #00e676;
  box-shadow: 0 0 15px rgba(0, 230, 118, 0.15);
  background: #000;
}

.native-textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 16px;
  font-family: inherit;
  resize: none;
  outline: none;
  padding: 8px 0;
  max-height: 120px;
  line-height: 1.5;
}

.math-field-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 18px;
  width: 100%;
  padding: 4px 0;
  outline: none;
  --caret-color: #00e676;
}

.toggle-mode-btn {
  width: 34px;
  height: 34px;
  margin-left: 8px;
  margin-bottom: 2px;
  border-radius: 50%;
  border: 1px solid #333;
  background: #1e1e24;
  color: #888;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toggle-mode-btn:active, 
.focused .toggle-mode-btn {
  border-color: #00e676;
  color: #00e676;
}
</style>