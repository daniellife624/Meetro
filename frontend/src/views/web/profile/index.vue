<template>
  <div class="profile-page p-8 max-w-4xl mx-auto bg-white shadow-lg rounded-xl my-10">
    <h1 class="text-3xl font-extrabold text-gray-800 mb-6 border-b pb-2">
      個人檔案設定 (User Profile)
    </h1>

    <div class="space-y-4">
      <p class="text-gray-600">
        歡迎來到您的個人資料頁面。您可以在這裡更新帳戶資訊、密碼或偏好設定。
      </p>
      <!-- 這是未來放置實際表單和邏輯的位置 -->
      <div class="p-4 border border-gray-200 rounded-lg">
        <p class="font-semibold">帳戶資訊</p>
        <p class="text-sm text-gray-500">未來您可以在這裡載入並編輯使用者資料。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 這裡將是用於管理用戶狀態、更新資料的邏輯
// 例如：
// import { ref } from 'vue';
// const username = ref('Meetro User');
</script>

<style scoped>
/* 頁面專屬的樣式 */
.profile-page {
  font-family: 'Inter', sans-serif;
}
</style>
