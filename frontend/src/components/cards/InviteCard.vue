<template>
  <div
    class="bg-white rounded-[20px] shadow-md border border-gray-100 transition hover:shadow-lg p-6 flex flex-col justify-between h-full"
  >
    <div class="space-y-3 mb-6">
      <h3 class="font-bold text-gray-800 text-xl border-b border-gray-100 pb-2 mb-3">
        挑選對象：{{ invite.senderName }}
      </h3>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-gray-700">
        <p class="text-sm font-medium">
          <span class="text-gray-500">性別：</span>{{ invite.senderGender }}
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
        <button
          @click="$emit('feedback')"
          class="flex-1 w-full px-2 py-2 rounded-full bg-[#198754] text-white text-sm font-bold hover:bg-[#146c43] transition-colors flex justify-center items-center"
        >
          填寫滿意度
        </button>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface InviteHistoryItem {
  id: number
  senderName: string
  senderGender: string
  stationName: string
  location: string
  status: 'pending' | 'confirmed'
}

defineProps<{
  invite: InviteHistoryItem
  type: 'pending' | 'confirmed'
}>()

defineEmits<{
  (e: 'view-details'): void
  (e: 'confirm'): void
  (e: 'decline'): void
  (e: 'feedback'): void
}>()
</script>

<style scoped></style>
