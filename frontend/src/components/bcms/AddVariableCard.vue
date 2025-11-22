<template>
  <button
    class="min-w-[280px] w-[280px] bg-[#CDCDCD] hover:bg-[#bfbfbf] rounded-2xl flex flex-col items-center justify-center shadow-inner transition-colors cursor-pointer group border-2 border-transparent hover:border-gray-400"
    @click="$emit('add')"
  >
    <div class="text-center space-y-2">
      <div
        class="text-5xl font-extrabold text-white group-hover:scale-110 transition-transform duration-300"
      >
        新 增
      </div>
      <div
        class="text-5xl font-extrabold text-white group-hover:scale-110 transition-transform duration-300"
      >
        參 數
      </div>
    </div>

    <div class="mt-4 text-white opacity-50 group-hover:opacity-100 transition">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-12 w-12"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
      </svg>
    </div>
  </button>
</template>

<script setup lang="ts">
defineEmits(['add'])
</script>
