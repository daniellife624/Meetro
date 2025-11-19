<template>
  <!-- 單一邀約項目卡片，供選擇方瀏覽 -->
  <div
    class="p-4 border border-gray-200 rounded-xl shadow-md flex justify-between items-start space-x-4 bg-white hover:shadow-lg transition-shadow duration-300"
  >
    <div class="flex-grow space-y-1">
      <div class="flex items-center space-x-2">
        <!-- 發送方頭像/圖示 -->
        <SvgItem name="user" size="20" class="text-green-600"></SvgItem>
        <span class="text-sm font-semibold text-gray-700">發送者: {{ invite.senderName }}</span>
      </div>

      <!-- 邀約日期 -->
      <p class="text-base text-gray-900 font-medium">
        邀約日期: <span class="text-green-700">{{ invite.date }} ({{ invite.day }})</span>
      </p>

      <!-- 邀約地點 -->
      <p class="text-sm text-gray-600 truncate">邀約地點: {{ invite.location }}</p>

      <!-- 聊天圖示 (假設用於標記新訊息或可聊天狀態) -->
      <div
        v-if="invite.hasChat"
        class="absolute top-4 right-4 bg-lime-500 text-white rounded-full p-1 shadow-lg"
      >
        <SvgItem name="comment-dots" size="18" class="animate-pulse"></SvgItem>
      </div>
    </div>

    <!-- 操作按鈕群組 -->
    <div class="flex flex-col space-y-2 ml-4 flex-shrink-0">
      <button
        @click="viewDetails"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
      >
        詳細資訊
      </button>
      <button
        @click="acceptInvite"
        class="px-4 py-2 text-sm font-medium text-white bg-green-500 rounded-full hover:bg-green-600 transition-colors shadow-md"
      >
        接受
      </button>
      <button
        @click="rejectInvite"
        class="px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-full hover:bg-red-600 transition-colors shadow-md"
      >
        刪除
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import SvgItem from '@/components/icons/SvgItem.vue'

// 定義邀約資料結構 (使用範例數據的欄位)
interface Invite {
  id: number
  senderName: string
  date: string // e.g., '2025/11/12'
  day: string // e.g., '三'
  location: string // e.g., '公館水岸廣場'
  hasChat: boolean // 模擬是否有新的聊天或已接受
}

interface Props {
  invite: Invite
}

const props = defineProps<Props>()

const emit = defineEmits(['view-details', 'accept', 'reject'])

const viewDetails = () => {
  emit('view-details', props.invite.id)
}

const acceptInvite = () => {
  // 實作接受邏輯，可能需要跳出確認彈窗
  emit('accept', props.invite.id)
}

const rejectInvite = () => {
  // 實作刪除/拒絕邏輯
  emit('reject', props.invite.id)
}
</script>
