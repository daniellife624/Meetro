<template>
  <div
    class="flex flex-col sm:flex-row bg-white rounded-[20px] shadow-md overflow-hidden border border-gray-100 transition hover:shadow-lg"
  >
    <div class="w-full sm:w-40 h-40 sm:h-auto relative flex-shrink-0">
      <img
        :src="invite.senderAvatar || 'https://picsum.photos/200'"
        alt="User Avatar"
        class="w-full h-full object-cover"
      />
    </div>

    <div class="flex-grow p-4 flex flex-col justify-between relative">
      <div class="space-y-2 mb-4">
        <h3 class="font-bold text-gray-800 text-lg">挑選對象：{{ invite.senderName }}</h3>
        <p class="text-sm font-medium text-gray-700">性別：{{ invite.senderGender }}</p>
        <p class="text-sm font-medium text-gray-700">選擇捷運站：{{ invite.stationName }}</p>
        <p class="text-sm font-bold text-gray-900">地點：{{ invite.location }}</p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <button
          @click="$emit('view-details')"
          class="px-6 py-2 rounded-full bg-[#9CA3AF] text-white text-sm font-bold hover:bg-gray-500 transition-colors"
        >
          更多細節
        </button>

        <template v-if="type === 'pending'">
          <button
            @click="$emit('confirm')"
            class="px-6 py-2 rounded-full bg-[#81c784] text-white text-sm font-bold hover:bg-[#286047] transition-colors"
          >
            確定赴約
          </button>
          <button
            @click="$emit('decline')"
            class="px-6 py-2 rounded-full bg-[#FCA5A5] text-white text-sm font-bold hover:bg-[#ef4444] transition-colors"
          >
            決定婉拒
          </button>
        </template>

        <template v-if="type === 'confirmed'">
          <button
            @click="$emit('feedback')"
            class="px-6 py-2 rounded-full bg-[#198754] text-white text-sm font-bold hover:bg-[#146c43] transition-colors"
          >
            填寫滿意度
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface InviteHistoryItem {
  id: number
  senderName: string
  senderGender: string
  senderAvatar?: string
  stationName: string
  location: string
  status: 'pending' | 'confirmed' // 用於判斷資料屬於哪個 Tab
  // ...其他詳細資料欄位
}

// 定義 Props
defineProps<{
  invite: InviteHistoryItem
  type: 'pending' | 'confirmed' // 決定顯示哪組按鈕
}>()

// 定義 Emits
defineEmits<{
  (e: 'view-details'): void
  (e: 'confirm'): void
  (e: 'decline'): void
  (e: 'feedback'): void
}>()
</script>

<style scoped>
/* 可根據需要微調 */
</style>
