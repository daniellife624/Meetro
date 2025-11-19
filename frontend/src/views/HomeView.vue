<template>
  <div class="p-8">
    <h2 class="text-4xl font-extrabold text-indigo-600 mb-4">歡迎使用 Meetro！</h2>
    <p class="text-xl text-gray-700">這是應用程式的主頁面。</p>

    <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 放置您的 BaseButton 組件，確認路由成功載入 -->
      <div class="bg-white p-6 rounded-xl shadow-lg">
        <h3 class="text-2xl font-semibold mb-3 text-gray-800">元件測試確認</h3>
        <!-- 確保 BaseButton 載入路徑正確 -->
        <!-- <BaseButton type="primary">路由測試成功</BaseButton> -->
      </div>
      <div class="bg-white p-6 rounded-xl shadow-lg">
        <h3 class="text-2xl font-semibold mb-3 text-gray-800">下一步</h3>
        <p class="text-gray-600">我們將開始創建活動卡片元件。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// import BaseButton from '@/components/BaseButton.vue' // 確保路徑是從根目錄開始 (使用 @)
</script>

<style scoped>
/* 頁面專屬樣式 */
</style>
