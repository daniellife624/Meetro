<template>
  <div
    class="flex bg-[#f1f8e9] p-4 rounded-xl shadow-lg border border-[#c8e6c9] transform transition duration-300 hover:shadow-xl hover:scale-[1.01] cursor-default items-start"
  >
    <div
      class="flex-shrink-0 w-10 h-10 bg-[#286047] text-white rounded-full flex items-center justify-center shadow-md mr-4"
    >
      <component v-if="icon" :is="icon" class="w-5 h-5" />
      <span v-else class="font-black text-lg">{{ step }}</span>
    </div>

    <div class="flex-grow">
      <h3 class="text-sm font-bold text-[#1b5e20] mb-1">{{ title }}</h3>
      <p class="text-xs text-gray-700 whitespace-pre-line leading-relaxed">
        {{ content }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Component } from 'vue'

// 定義明確的 Props，不做任何複雜運算
defineProps<{
  step: number
  title: string
  content: string
  icon?: Component // 可選屬性
}>()
</script>

<style scoped></style>
