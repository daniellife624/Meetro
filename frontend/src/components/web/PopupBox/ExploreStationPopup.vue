<template>
  <div class="space-y-6">
    <p class="text-md text-gray-700">
      您選擇了探索 <span class="text-red-500 font-bold">{{ selectedStation }}</span> 站。
      請選擇您希望在這個站點扮演的角色：
    </p>

    <div class="space-y-4">
      <div
        v-for="option in roleOptions"
        :key="option.key"
        @click="selectedRole = option.key"
        :class="{
          'border-[#286047] bg-[#f1f8e9] shadow-inner': selectedRole === option.key,
          'border-gray-200 hover:border-gray-400 hover:bg-gray-50': selectedRole !== option.key,
        }"
        class="flex items-start p-4 border-2 rounded-xl cursor-pointer transition duration-200"
      >
        <div class="mt-1 mr-3">
          <Send v-if="option.key === 'sender'" size="24" class="text-[#286047]" />
          <Users v-else size="24" class="text-blue-500" />
        </div>
        <div>
          <p class="font-bold text-gray-800">{{ option.title }}</p>
          <p class="text-xs text-gray-500">{{ option.description }}</p>
        </div>
        <div v-if="selectedRole === option.key" class="ml-auto p-1 rounded-full bg-[#286047]">
          <Check size="16" class="text-white" />
        </div>
      </div>
    </div>

    <p class="text-center pt-2">
      <span class="font-bold text-[#286047]">您選定的角色是：</span>
      <span
        :class="selectedRole === 'sender' ? 'text-[#286047]' : 'text-blue-600'"
        class="font-extrabold"
      >
        {{ selectedRole === 'sender' ? '發送方' : '選擇方' }}
      </span>
    </p>

    <button
      @click="handleConfirm"
      class="w-full mt-4 py-3 bg-[#286047] text-white font-bold rounded-xl shadow-lg hover:bg-green-700 transition duration-300"
    >
      挑選景點（作為 {{ selectedRole === 'sender' ? '發送方' : '選擇方' }}）
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SvgItem from '@/components/icons/SvgItem.vue'

const props = defineProps<{
  selectedStation: string
}>()

const emit = defineEmits<{
  (e: 'explore', station: string, role: 'sender' | 'receiver'): void
}>()

const selectedRole = ref<'sender' | 'receiver'>('sender') // 'sender' (發送方) or 'receiver' (選擇方)

const roleOptions = [
  {
    key: 'sender',
    title: '發送方 (想找人一起參與)',
    description: '主動發起邀約，設定活動內容與時間。',
  },
  {
    key: 'receiver',
    title: '選擇方 (尋找有趣活動)',
    description: '瀏覽他人發起的邀約，選擇感興趣的參與。',
  },
]

const handleConfirm = () => {
  // 觸發 @explore 事件，將站點和選定的角色回傳給父元件 (MeetroHomePage.vue)
  emit('explore', props.selectedStation, selectedRole.value)
}
</script>

<style scoped>
/* 自定義選擇器樣式 */
</style>
