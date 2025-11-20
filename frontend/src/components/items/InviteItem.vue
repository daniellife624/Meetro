<template>
  <div
    class="flex items-center justify-between w-full p-5 bg-white border-2 border-[#286047] border-r-0 rounded-l-[50px] rounded-r-none shadow-sm hover:shadow-md transition-all duration-300"
  >
    <div class="flex flex-col space-y-2 pl-6 flex-grow">
      <div class="text-base font-bold text-gray-800 tracking-wide">
        發送對象 : {{ invite.senderName }}
      </div>

      <div class="text-base font-bold text-gray-800 tracking-wide">
        邀約日期 : {{ invite.date }} ({{ invite.day }})
      </div>

      <div class="text-base font-bold text-gray-800 tracking-wide">
        邀約地點 : {{ invite.location }}
      </div>

      <span v-if="invite.hasChat" class="inline-block text-xs font-normal text-blue-500 pt-1">
        * 已建立聊天
      </span>
    </div>

    <div class="flex items-center gap-3 flex-shrink-0 pl-4">
      <button
        @click="viewDetails"
        class="px-6 py-2 text-white font-bold bg-gray-400 hover:bg-gray-500 rounded-full shadow transition-colors text-sm min-w-[90px]"
      >
        詳細資訊
      </button>

      <button
        @click="acceptInvite"
        class="px-6 py-2 text-white font-bold bg-[#50C895] hover:bg-[#3da87a] rounded-full shadow transition-colors text-sm min-w-[80px]"
      >
        接受
      </button>

      <button
        @click="rejectInvite"
        class="px-6 py-2 text-white font-bold bg-[#FF5D5D] hover:bg-[#e04646] rounded-full shadow transition-colors text-sm min-w-[80px]"
      >
        刪除
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
// Script 部分保持不變，邏輯相同
interface Invite {
  id: number
  senderName: string
  date: string
  day: string
  location: string
  hasChat: boolean
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
  emit('accept', props.invite.id)
}

const rejectInvite = () => {
  emit('reject', props.invite.id)
}
</script>

<style scoped>
/* 如果你想讓左邊的圓角更圓或更像膠囊，可以調整 rounded-l-[50px] 的數值 */
</style>
