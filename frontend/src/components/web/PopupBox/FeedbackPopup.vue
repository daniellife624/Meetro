<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 backdrop-filter backdrop-blur-sm"
    @click.self="close"
  >
    <div
      class="bg-white w-full max-w-md mx-4 md:mx-0 rounded-lg shadow-2xl relative p-6 md:p-8 animate-fadeIn"
    >
      <button
        @click="close"
        class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <h2 class="text-2xl font-bold mb-4 text-[#286047] border-b pb-2">請為本次邀約評分</h2>
      <p class="text-sm text-gray-500 mb-6">您的評分（0-100）將影響對方未來的匹配權重。</p>

      <div class="space-y-4">
        <label for="rating-slider" class="block text-lg font-semibold text-gray-700">
          滿意度評分：<span class="text-[#008659]">{{ rating }}</span> / 100
        </label>

        <input
          id="rating-slider"
          type="range"
          min="0"
          max="100"
          step="1"
          v-model.number="rating"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer range-lg transition-colors"
          :class="{
            'range-green': rating > 50,
            'range-orange': rating <= 50,
          }"
        />

        <div class="flex justify-between text-sm text-gray-500 mt-1">
          <span>0 (不滿意)</span>
          <span>100 (非常滿意)</span>
        </div>

        <input
          type="number"
          v-model.number="rating"
          min="0"
          max="100"
          class="w-24 mt-2 p-2 border border-gray-300 rounded-lg text-center font-mono text-lg focus:ring-[#286047] focus:border-[#286047]"
        />
      </div>

      <div class="flex justify-end gap-3 mt-8">
        <button
          @click="close"
          class="px-6 py-2 border border-gray-300 rounded-full text-gray-600 hover:bg-gray-100 transition"
        >
          取消
        </button>
        <button
          @click="submitFeedback"
          :disabled="isSubmitting"
          class="px-6 py-2 bg-[#008659] text-white font-bold rounded-full hover:bg-green-700 transition disabled:bg-gray-400"
        >
          {{ isSubmitting ? '提交中...' : '確認提交' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import request from '@/utils/request'

// 假設從 history.vue 傳入 matchId
const props = defineProps<{
  matchId: number
}>()

const emit = defineEmits(['close', 'submitted'])

const rating = ref(100) // 預設滿分
const isSubmitting = ref(false)

const close = () => {
  emit('close')
}

const submitFeedback = async () => {
  if (rating.value < 0 || rating.value > 100) {
    alert('評分必須在 0 到 100 之間！')
    return
  }

  isSubmitting.value = true

  try {
    const res = await request.post(`/api/matches/${props.matchId}/feedback`, {
      rating: rating.value,
    })

    if (res && res.status === 'success') {
      alert(`滿意度提交成功！\n當前配對狀態: ${res.feedback_status}`)
    } else {
      // 處理成功但返回結構不對的極端情況
      alert('提交成功，但響應格式異常。')
    }
    // 通知父組件 (history.vue) 資料已更新
    emit('submitted', { matchId: props.matchId, rating: rating.value })
    close()
  } catch (error: any) {
    console.error('Feedback Submission Failed:', error)

    // 顯示後端返回的 detail 訊息 (如果有的話)
    const errorDetail = error.detail || error.message || '未知錯誤'
    alert('提交失敗：' + errorDetail)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.2s ease-out forwards;
}

/* 自定義拉桿樣式 */
input[type='range'] {
  -webkit-appearance: none;
  height: 8px;
}

input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #008659;
  cursor: pointer;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  margin-top: -6px;
}

/* 根據評分改變顏色 (僅為視覺效果) */
.range-green::-webkit-slider-thumb {
  background: #4caf50;
}
.range-orange::-webkit-slider-thumb {
  background: #ff9800;
}
</style>
