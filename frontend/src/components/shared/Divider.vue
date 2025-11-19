<template>
  <!-- 模擬垂直分隔線 -->
  <div class="w-[1px] bg-gray-300 mx-3" :style="{ height: style?.height || '24px' }"></div>
</template>

<script setup lang="ts">
// 接收 style 屬性，允許設定高度
defineProps<{
  style?: { height: string }
}>()
</script>
