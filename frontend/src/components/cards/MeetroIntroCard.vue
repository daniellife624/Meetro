<template>
  <div
    class="flex bg-[#f1f8e9] p-4 rounded-xl shadow-lg border border-[#c8e6c9] transform transition duration-300 hover:shadow-xl hover:scale-[1.01] cursor-default"
  >
    <div
      class="flex-shrink-0 w-10 h-10 bg-[#286047] text-white rounded-full flex items-center justify-center font-black text-lg mr-4 shadow-md"
    >
      {{ step }}
    </div>
    <!-- 內容 -->
    <div>
      <h3 class="text-sm font-bold text-[#1b5e20] mb-1">{{ title }}</h3>
      <p class="text-xs text-gray-700 whitespace-pre-line">{{ content }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  step: number
  text: string
}>()

// 修正點：加入 (props.text || '') 防禦性檢查，避免在 props.text 是 undefined 或 null 時呼叫 .split()
const textParts = computed(() => (props.text || '').split('\n'))

// 修正點：為 title 加入 fallback 處理，避免在初始化時 textParts.value[0] 為空
const title = computed(() => textParts.value[0] || '載入中...')
const content = computed(() => textParts.value.slice(1).join('\n'))
</script>

<style scoped></style>
