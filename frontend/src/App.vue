<script setup lang="ts">
import { RouterView } from 'vue-router'
// 1. 確保正確導入 GlobalLoadingOverlay.vue
// 假設路徑是 @/components/shared/GlobalLoadingOverlay.vue
import GlobalLoadingOverlay from '@/components/shared/GlobalLoadingOverlay.vue'
</script>

<template>
  <!-- 這是整個應用程式的根容器 -->
  <div class="min-h-screen flex flex-col">
    <!-- RouterView 將根據當前路由渲染對應的 Layout 或 Page -->
    <RouterView />

    <!-- 2. 在模板中使用 GlobalLoadingOverlay 組件 -->
    <!-- 放置在最頂層，以便它可以覆蓋應用程式中的所有內容 -->
    <GlobalLoadingOverlay />
  </div>
</template>

<style scoped>
/* 這裡可以放 App.vue 的特定樣式 */
</style>
