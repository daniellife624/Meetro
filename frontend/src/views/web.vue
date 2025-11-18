<template>
  <div class="web-view">
    <!-- 這個組件通常是網頁前端主要的佈局容器 -->
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
// 您可以在這裡加入網頁端全域共用的邏輯或佈局
</script>

<style scoped>
.web-view {
  /* 確保佈局佔滿整個視口 */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
