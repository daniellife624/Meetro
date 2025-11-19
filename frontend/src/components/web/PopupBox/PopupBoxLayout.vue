<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm p-4"
  >
    <div
      class="bg-white rounded-2xl w-full max-w-lg shadow-2xl transform transition-all duration-300 scale-100 opacity-100"
    >
      <!-- 標題與關閉按鈕 -->
      <div class="flex justify-between items-center p-5 border-b border-gray-200">
        <h2 class="text-xl font-extrabold text-[#286047]">{{ title }}</h2>
        <button
          @click="cancelCallback"
          class="text-gray-400 hover:text-gray-600 transition p-1 rounded-full hover:bg-gray-100"
          aria-label="Close popup"
        >
          <!-- 使用 SvgItem 替代 X -->
          <SvgItem name="x" size="6" class="w-6 h-6" />
        </button>
      </div>

      <!-- 內容區域 -->
      <div class="p-6">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 導入 SvgItem
import SvgItem from '@/components/icons/SvgItem.vue'

defineProps<{
  title: string
  confirmText: string
  cancelCallback: () => void
  confirmCallback: () => void // 這裡的 callback 在主頁面被設置為空，實際邏輯在 slot 內處理
  type?: string // 未使用，但保留
  useForm?: boolean // 未使用，但保留
  id?: string // 未使用，但保留
}>()
</script>

<style scoped></style>
