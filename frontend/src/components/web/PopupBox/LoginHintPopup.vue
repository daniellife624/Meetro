<template>
  <div class="text-center py-2 px-4 space-y-6">
    <div class="flex justify-center">
      <div
        class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center animate-bounce"
      >
        <SvgItem name="login" size="10" class="text-[#008659]" />
      </div>
    </div>

    <div class="space-y-2">
      <h3 class="text-xl font-bold text-gray-800">您尚未登入</h3>
      <p class="text-gray-600 leading-relaxed">
        快去註冊、登入，才能享受 Meetro 的完整探索與配對服務喔！
      </p>
    </div>

    <div class="flex flex-col gap-3 pt-2">
      <button
        @click="$emit('go-login')"
        class="w-full py-3 bg-[#008659] text-white font-bold rounded-xl shadow-md hover:bg-green-800 transition duration-300 flex justify-center items-center gap-2"
      >
        <span>前往登入 / 註冊</span>
        <SvgItem name="login" size="5" />
      </button>

      <button
        @click="$emit('cancel')"
        class="w-full py-3 bg-gray-100 text-gray-600 font-bold rounded-xl hover:bg-gray-200 transition duration-300"
      >
        先逛逛地圖就好
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import SvgItem from '@/components/icons/SvgItem.vue'

// 定義事件，通知父組件 (index.vue) 要做什麼
defineEmits<{
  (e: 'go-login'): void
  (e: 'cancel'): void
}>()
</script>
