<template>
  <!-- 容器使用相對定位，以便下拉菜單能絕對定位在按鈕下方 -->
  <div
    class="relative inline-block h-full"
    @mouseenter="isHovering = true"
    @mouseleave="isHovering = false"
  >
    <!-- 主要的導航按鈕/觸發區域 -->
    <button
      class="h-full flex items-center justify-center space-x-2 text-white px-4 transition-all duration-300 bg-transparent hover:bg-white/10 focus:outline-none"
    >
      <!-- 導航圖標和文字內容 -->
      <slot name="default">導航按鈕</slot>
    </button>

    <Transition
      name="expand"
      @before-enter="handleBeforeEnter"
      @enter="handleEnter"
      @before-leave="handleBeforeLeave"
      @leave="handleLeave"
      @after-enter="handleAfterEnter"
    >
      <!-- 下拉菜單容器 -->
      <div
        class="expand-menu absolute top-full right-0 mt-0.5 bg-white shadow-2xl rounded-lg z-50 overflow-hidden min-w-[180px] border border-gray-200"
        v-show="isHovering"
      >
        <slot name="menu"></slot>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { RendererElement } from 'vue'

// 控制菜單的顯示狀態
const isHovering = ref(false)

/**
 * Transition Hook: 在元素進入或離開前執行。
 * @param el - DOM 元素
 */
const handleBeforeEnter = (el: RendererElement) => {
  el.style.height = '0'
  el.style.opacity = '0'
  el.style.transition = '' // 清除 transition
}

/**
 * Transition Hook: 在元素進入前執行，用於定義擴展動畫。
 * (與 handleBeforeEnter 邏輯相同，但名稱與 leave 保持對應)
 * @param el - DOM 元素
 */
const handleBeforeLeave = (el: RendererElement) => {
  // 在離開前，設置元素的高度為其實際高度，為收合動畫準備
  el.style.height = el.scrollHeight + 'px'
  el.style.opacity = '1'
  el.style.transition = '' // 清除 transition
}

/**
 * Transition Hook: 在元素進入時執行，用於定義擴展動畫。
 * @param el - DOM 元素
 * @param done - 呼叫此函數以結束過渡
 */
const handleEnter = (el: RendererElement, done: () => void) => {
  // 設置過渡屬性和時長
  el.style.transition = 'height 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), opacity 0.2s ease-in'
  // 設置最終高度
  el.style.height = el.scrollHeight + 'px'
  el.style.opacity = '1'

  // 監聽過渡結束事件，以清理樣式
  el.addEventListener('transitionend', done, { once: true })
}

/**
 * Transition Hook: 在元素進入後執行，用於清理樣式。
 * @param el - DOM 元素
 */
const handleAfterEnter = (el: RendererElement) => {
  // 清除行內樣式
  el.style.height = ''
  el.style.transition = ''
}

/**
 * Transition Hook: 在元素離開時執行，用於定義收合動畫。
 * @param el - DOM 元素
 * @param done - 呼叫此函數以結束過渡
 */
const handleLeave = (el: RendererElement, done: () => void) => {
  // 設置過渡屬性
  el.style.transition = 'height 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), opacity 0.3s ease-out'

  // 設置目標高度 (收合到 0)
  el.style.height = '0'
  el.style.opacity = '0'

  // 監聽過渡結束事件
  el.addEventListener('transitionend', done, { once: true })
}
</script>

<style scoped>
/* 樣式由 Tailwind CSS 處理 */
</style>
