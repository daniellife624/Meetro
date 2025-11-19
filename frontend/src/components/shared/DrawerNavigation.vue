<template>
  <!-- 主抽屜容器，使用 fixed 定位和 Tailwind/Windi CSS 類別控制開關狀態與過渡效果 -->
  <div
    :class="[
      'fixed inset-0 z-50 transition-transform duration-300',
      isDrawerOpen ? 'translate-x-0' : '-translate-x-full',
    ]"
  >
    <!-- 1. 遮罩層 (點擊關閉) -->
    <div class="absolute inset-0 bg-black/50" @click="closeDrawer" aria-label="Close menu"></div>

    <!-- 2. 抽屜內容面板 -->
    <div class="relative w-64 max-w-xs h-full bg-white shadow-2xl p-4 flex flex-col">
      <!-- 抽屜標頭 / 關閉按鈕 -->
      <div class="flex justify-between items-center pb-4 border-b border-gray-100">
        <h2 class="text-xl font-bold text-gray-800">導航選單</h2>
        <button @click="closeDrawer" class="text-gray-500 hover:text-red-500 transition-colors">
          <!-- 關閉圖標 (Lucide X) -->
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="lucide lucide-x"
          >
            <path d="M18 6 6 18" />
            <path d="m6 6 12 12" />
          </svg>
        </button>
      </div>

      <!-- 導航連結 -->
      <nav class="mt-4 space-y-2 flex-grow">
        <a
          href="#"
          class="block p-2 rounded-lg text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
        >
          首頁
        </a>
        <a
          href="#"
          class="block p-2 rounded-lg text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
        >
          個人檔案
        </a>
        <a
          href="#"
          class="block p-2 rounded-lg text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
        >
          設定
        </a>
        <!-- 您可以在此處新增更多連結 -->
      </nav>

      <!-- 底部資訊 (可選) -->
      <div class="pt-4 border-t border-gray-100 text-sm text-gray-500">目前登入使用者.</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Ref } from 'vue'

// 定義 props，以便從父組件接收 modelValue (控制開關)
const props = defineProps<{
  modelValue: boolean
}>()

// 定義 emit，用於更新父組件的 v-model 狀態
const emit = defineEmits(['update:modelValue'])

const isDrawerOpen: Ref<boolean> = ref(props.modelValue)

// 監聽 modelValue 的外部變化，同步抽屜狀態
watch(
  () => props.modelValue,
  (newVal) => {
    isDrawerOpen.value = newVal
  },
)

// 關閉抽屜並通知父組件
const closeDrawer = () => {
  isDrawerOpen.value = false
  emit('update:modelValue', false)
}
</script>

<!-- 
***重要修正：此處已移除 lang="scss" 屬性。***
現在這個區塊只會使用標準 CSS，不會再觸發 sass-embedded 依賴錯誤。
所有樣式都透過 Windi CSS 類別處理。
-->
<style scoped>
/* 這裡可以放置任何需要自定義的標準 CSS */
</style>
