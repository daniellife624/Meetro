<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 text-center p-10 bg-white shadow-2xl rounded-xl">
      <!-- 錯誤代碼 -->
      <h1
        class="text-9xl font-extrabold text-indigo-600 tracking-wider transition-colors duration-300"
      >
        404
      </h1>

      <!-- 標題 -->
      <p class="text-3xl font-semibold text-gray-800">找不到頁面</p>

      <!-- 說明文字 -->
      <p class="mt-2 text-sm text-gray-500">您嘗試訪問的頁面不存在，或已被移動。</p>

      <!-- 返回首頁按鈕 -->
      <router-link
        to="/"
        class="mt-6 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-150"
      >
        返回首頁
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// 確保這是一個乾淨的 setup 區塊，沒有不必要的複雜邏輯或導入錯誤。
</script>

<style scoped>
/* 頁面專屬樣式，確保沒有影響編譯的錯誤語法 */
</style>
