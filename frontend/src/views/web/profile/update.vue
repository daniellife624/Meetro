<template>
  <div class="profile-update-page p-8 max-w-2xl mx-auto bg-white shadow-xl rounded-xl my-10">
    <h1 class="text-3xl font-extrabold text-indigo-700 mb-8 border-b pb-3">更新個人檔案資訊</h1>

    <form class="space-y-6">
      <!-- 範例輸入欄位：用戶名 -->
      <div>
        <label for="username" class="block text-sm font-medium text-gray-700"
          >用戶名 (Username)</label
        >
        <input
          type="text"
          id="username"
          value="Meetro User"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
      </div>

      <!-- 範例輸入欄位：電子郵件 -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">電子郵件 (Email)</label>
        <input
          type="email"
          id="email"
          value="user@meetro.com"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
      </div>

      <!-- 儲存按鈕 -->
      <button
        type="submit"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
      >
        儲存變更
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
// 這裡將是用於處理表單提交、API 調用和狀態管理的邏輯。
// 引入必要的 hooks，例如：
// import { ref } from 'vue';
</script>

<style scoped>
/* 樣式保持簡潔，依賴 Tailwind CSS */
</style>
