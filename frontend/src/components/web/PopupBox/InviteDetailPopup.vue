<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 backdrop-filter backdrop-blur-sm"
    @click.self="close"
  >
    <div
      class="bg-white w-full max-w-2xl mx-4 md:mx-0 rounded-lg shadow-2xl relative p-8 md:p-10 animate-fadeIn"
    >
      <button
        @click="close"
        class="absolute top-6 right-6 text-gray-800 hover:text-gray-600 transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-8 w-8"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </button>

      <div class="space-y-5 text-lg text-gray-800 tracking-wide">
        <div class="flex flex-col md:flex-row md:items-start">
          <span class="font-bold min-w-[180px]">發送對象：</span>
          <span class="text-gray-700">{{ invite.senderName }}</span>
        </div>

        <div class="flex flex-col md:flex-row md:items-start">
          <span class="font-bold min-w-[180px]">邀約活動主題 (事)：</span>
          <span class="text-gray-700 flex-1">{{ invite.title }}</span>
        </div>

        <div class="flex flex-col md:flex-row md:items-start">
          <span class="font-bold min-w-[180px]">邀約日期：</span>
          <span class="text-gray-700">{{ invite.date }} ({{ invite.day }})</span>
        </div>

        <div class="flex flex-col md:flex-row md:items-start">
          <span class="font-bold min-w-[180px]">捷運站：</span>
          <span class="text-[#008659] font-bold">{{ invite.stationName }}</span>
        </div>

        <div class="flex flex-col md:flex-row md:items-start">
          <span class="font-bold min-w-[180px]">邀約地點：</span>
          <span class="text-gray-700">{{ invite.location }}</span>
        </div>

        <div class="flex flex-col md:flex-row md:items-start">
          <span class="font-bold min-w-[180px]">Google Map：</span>
          <div class="flex-1 overflow-hidden">
            <a
              :href="invite.googleMapLink"
              target="_blank"
              rel="noopener noreferrer"
              class="text-gray-600 underline hover:text-blue-600 break-all text-base leading-relaxed block"
            >
              {{ invite.googleMapLink || '無提供連結' }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

// 這裡定義資料介面，需與 ReceiverView 傳入的一致
interface InviteDetail {
  senderName: string
  title: string
  date: string
  day: string
  stationName: string
  location: string
  googleMapLink: string
}

defineProps<{
  invite: InviteDetail
}>()

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}
</script>

<style scoped>
/* 簡單的淡入動畫 */
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
</style>
