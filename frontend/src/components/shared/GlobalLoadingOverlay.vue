<template>
  <!-- 這是全域載入遮罩組件，根據 Pinia Store 的狀態顯示 -->
  <Transition name="fade">
    <div
      v-if="loadingStore.isLoading"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-70 backdrop-blur-sm transition-opacity duration-300"
    >
      <div class="flex flex-col items-center p-6 bg-white rounded-xl shadow-2xl">
        <!-- Lottie Placeholder for Animation -->
        <div class="w-16 h-16 mb-4">
          <!-- 由於我們在 main.ts 中移除了 Lottie，這裡先用 SVG 佔位 -->
          <svg
            class="animate-spin text-indigo-600"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        </div>

        <p class="text-lg font-semibold text-gray-700 select-none">
          {{ loadingStore.loadingMessage || '載入中...' }}
        </p>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { useLoadingStore } from '@/stores/modules/loading.ts' // 導入 Pinia Store

const loadingStore = useLoadingStore()
</script>

<style scoped>
/* 定義過渡動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
