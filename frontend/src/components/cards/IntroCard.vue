<template>
  <!-- 卡片外框：使用設計稿中的淺綠色邊框和圓角 -->
  <div
    class="p-5 border-2 border-[#81C784] rounded-xl bg-white shadow-sm transition duration-300 hover:shadow-lg"
  >
    <p class="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed font-medium">
      {{ text }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{
  /**
   * 卡片要顯示的文字內容 (包含 STEP 標題和內容)
   */
  text: string
  /**
   * 步驟編號 (例如: 1, 2, 3...) - 此版本未使用，但保留屬性
   */
  step: number
}>()
</script>

<style scoped>
/* 保持簡潔 */
</style>
