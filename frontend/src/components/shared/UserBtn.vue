<template>
  <button
    class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-200 text-gray-700 font-bold hover:ring-2 hover:ring-blue-500 transition duration-150"
    title="Profile"
    @click="router.push({ name: 'Profile' })"
  >
    <!-- 這裡可以放使用者頭像或首字母 -->
    <svg
      class="w-6 h-6"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
      ></path>
    </svg>
  </button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
</script>
