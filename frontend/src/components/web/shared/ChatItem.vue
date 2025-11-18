<template>
  <!-- ChatItem 用於顯示單條聊天訊息 -->
  <div class="chat-item p-2">
    <!-- 這裡將是聊天訊息的實際內容 -->
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
// 這是 ChatItem 組件，目前為一個佔位用的空殼。
// 在後續開發中，您可以在此定義 props（如 message, sender, timestamp 等）
// 以及相關的邏輯。
</script>

<style scoped>
/* 可以在這裡添加 ChatItem 的特定樣式 */
.chat-item {
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
