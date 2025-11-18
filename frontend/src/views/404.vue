<script setup lang="ts">
import { ref } from 'vue'
// ----------------------------------------------------
// 修正點：從具名導入 { Vue3Lottie } 改為預設導入 Vue3Lottie
import Vue3Lottie from 'vue3-lottie'
// ----------------------------------------------------

// 導入您的 Lottie JSON 動畫文件
// 假設您有一個 Lottie 404 動畫在 assets/lottie-404.json
import animationData from '@/assets/lottie-404.json'

const defaultOptions = {
  animationData: animationData,
  loop: true,
}

const _hoisted_3 = { class: 'w-full h-80 mx-auto' }

// ... 其他代碼 ...
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4 bg-gray-50 text-gray-800">
    <div class="max-w-md w-full text-center">
      <h1 class="text-9xl font-extrabold text-indigo-600 mb-4">404</h1>
      <p class="text-2xl md:text-3xl font-light mb-6">Oops! 頁面走丟了。</p>

      <!-- Lottie 動畫容器 -->
      <div class="w-full h-80 mx-auto mb-8">
        <Vue3Lottie
          :animationLink="defaultOptions.animationData"
          :loop="defaultOptions.loop"
          :autoPlay="true"
        />
      </div>

      <router-link
        to="/"
        class="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 transition duration-300"
      >
        返回首頁
      </router-link>
    </div>
  </div>
</template>

<style scoped>
/* 頁面特定樣式 (如果需要) */
</style>
