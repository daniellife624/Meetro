<template>
  <div
    class="bg-white rounded-[20px] shadow-md border border-gray-100 transition hover:shadow-lg p-6 flex flex-col justify-between h-full"
  >
    <div class="space-y-3 mb-6">
      <h3 class="font-bold text-gray-800 text-xl border-b border-gray-100 pb-2 mb-3">
        挑選對象：{{ invite.partnerName }}
      </h3>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-gray-700">
        <p class="text-sm font-medium">
          <span class="text-gray-500">性別：</span>{{ invite.partnerGender }}
        </p>
        <p class="text-sm font-medium">
          <span class="text-gray-500">選擇捷運站：</span>{{ invite.stationName }}
        </p>
        <p class="text-sm font-bold sm:col-span-2">
          <span class="text-gray-500 font-medium">地點：</span>{{ invite.location }}
        </p>
      </div>
    </div>

    <div class="flex items-center gap-3 mt-auto w-full">
      <button
        @click="$emit('view-details')"
        class="flex-1 w-full px-2 py-2 rounded-full bg-gray-400 text-white text-sm font-bold hover:bg-gray-500 transition-colors flex justify-center items-center"
      >
        更多細節
      </button>

      <template v-if="type === 'pending'">
        <button
          @click="$emit('confirm')"
          class="flex-1 w-full px-2 py-2 rounded-full bg-[#50C895] text-white text-sm font-bold hover:bg-[#3da87a] transition-colors flex justify-center items-center"
        >
          確定赴約
        </button>
        <button
          @click="$emit('decline')"
          class="flex-1 w-full px-2 py-2 rounded-full bg-[#FF8A80] text-white text-sm font-bold hover:bg-[#ff5252] transition-colors flex justify-center items-center"
        >
          決定婉拒
        </button>
      </template>

      <template v-if="type === 'confirmed'">
        <template v-if="!isRated">
          <button
            @click="$emit('feedback')"
            class="flex-1 w-full px-2 py-2 rounded-full bg-[#198754] text-white text-sm font-bold hover:bg-[#146c43] transition-colors flex justify-center items-center"
          >
            填寫滿意度 模擬下一次邀約成功率
          </button>
        </template>
        <template v-else>
          <div
            class="flex-1 w-full text-center py-2 text-sm font-bold text-[#008659] border border-[#d4edda] rounded-full bg-[#E8F5E9]"
          >
            已提交評分
          </div>
        </template>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// 介面必須與後端 MatchItemResponse 和 history.vue 傳入的數據匹配
export interface InviteHistoryItem {
  id: number
  partnerName: string
  partnerGender: string // 來自後端 MatchItemResponse
  stationName: string
  location: string
  status: 'pending' | 'confirmed' | 'rejected' | string
  sender_rating: number | null
  receiver_rating: number | null
  is_current_user_sender: boolean // 來自後端
}

const props = defineProps<{
  invite: InviteHistoryItem
  type: 'pending' | 'confirmed'
}>()

defineEmits<{
  (e: 'view-details'): void
  (e: 'confirm'): void
  (e: 'decline'): void
  (e: 'feedback'): void // 觸發填寫滿意度彈窗
}>()

// 🚨 核心邏輯：判斷當前使用者是否已評分
const isRated = computed(() => {
  if (props.type !== 'confirmed') return false

  // 如果是 Sender，檢查 sender_rating
  if (props.invite.is_current_user_sender) {
    return props.invite.sender_rating !== null
  }
  // 如果是 Receiver，檢查 receiver_rating
  else {
    return props.invite.receiver_rating !== null
  }
})
</script>

<style scoped></style>
