<template>
  <div
    class="flex items-center justify-between w-full p-6 bg-white border border-[#286047] border-r-0 rounded-l-[50px] rounded-r-none shadow-sm hover:shadow-md transition-all duration-300 group"
  >
    <div class="flex flex-col space-y-2 pl-6 flex-grow">
      <div class="text-lg font-bold text-gray-800 tracking-wide">
        發送對象 : {{ invite.senderName }}
      </div>

      <div class="text-lg font-bold text-gray-800 tracking-wide">
        邀約日期 : {{ invite.date }} ({{ invite.day }})
      </div>

      <div class="text-lg font-bold text-gray-800 tracking-wide">
        邀約地點 : {{ invite.location }}
      </div>

      <span v-if="invite.hasChat" class="inline-block text-sm font-normal text-blue-500 pt-1">
        * 已建立聊天
      </span>
    </div>

    <div class="flex items-center gap-4 flex-shrink-0 pl-4">
      <button
        @click="viewDetails"
        class="px-8 py-2.5 text-white font-bold bg-gray-400 hover:bg-gray-500 rounded-full shadow transition-transform transform active:scale-95 text-base min-w-[110px]"
      >
        詳細資訊
      </button>

      <button
        @click="acceptInvite"
        class="px-8 py-2.5 text-white font-bold bg-[#50C895] hover:bg-[#3da87a] rounded-full shadow transition-transform transform active:scale-95 text-base min-w-[100px]"
      >
        接受
      </button>

      <button
        @click="rejectInvite"
        class="px-8 py-2.5 text-white font-bold bg-[#FF5D5D] hover:bg-[#e04646] rounded-full shadow transition-transform transform active:scale-95 text-base min-w-[100px]"
      >
        刪除
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
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
