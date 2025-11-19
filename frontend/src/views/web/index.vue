<template>
  <div class="flex flex-row h-full w-full bg-gray-100">
    <!-- Left -->
    <div class="w-1/3 bg-black p-6 flex flex-col">
      <!-- 標題區塊：固定高度 (使用深綠色 #286047) -->
      <h1 class="text-2xl font-extrabold mb-4 text-[#286047] border-b-2 border-[#E8F5E9] pb-3">
        Meetro 步驟指南
      </h1>
      <div class="intro-cards-scroll-area flex-grow overflow-y-auto pr-3">
        <div class="space-y-6">
          <IntroCard
            v-for="(content, index) in introContents"
            :key="index"
            :text="content"
            :step="index + 1"
          />
        </div>
      </div>
    </div>

    <!-- Right -->
    <div class="flex flex-col w-2/3 p-6 relative">
      <!-- 右上角的主標題和按鈕 -->
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-3xl font-extrabold text-[#286047]">捷運 松山新店線 地圖</h1>
        <!-- 按鈕使用設計稿中的綠色和圓角 -->
        <button
          class="px-6 py-2 bg-[#286047] text-white font-bold rounded-full shadow-lg hover:bg-green-700 transition duration-300"
        >
          開始探索 公館
        </button>
      </div>

      <!-- 地圖顯示區域 (佔大部分空間) -->
      <!-- 淺綠色背景 #E8F5E9 模擬地圖底圖，帶有圓角和陰影 -->
      <div
        class="flex-grow bg-[#E8F5E9] border border-[#C8E6C9] rounded-xl shadow-inner mb-6 flex items-center justify-center relative"
      >
        <!-- 模擬地圖線路圖內容 -->
        <div class="text-center">
          <p class="text-xl font-semibold text-[#286047] mb-4">
            [地圖元件將在此處載入，顯示松山新店線]
          </p>
          <!-- 模擬線路圖 (深綠色) -->
          <div
            class="bg-[#286047] h-12 w-[800px] max-w-full rounded-full flex items-center justify-between px-8 mx-auto"
          >
            <span class="text-white text-xs">新店</span>
            <span class="text-white text-xs">公館</span>
            <span class="text-white text-xs">南京復興</span>
            <span class="text-white text-xs">松山</span>
          </div>
        </div>

        <!-- 模擬松山終點站標記 -->
        <div
          class="absolute right-4 top-1/2 -translate-y-1/2 bg-[#286047] text-white p-3 rounded-l-full font-bold"
        >
          松山
        </div>
      </div>

      <!-- 底部資訊欄：選定的站點資訊 (公館站) -->
      <div class="flex justify-between items-end">
        <!-- 左下方：站點景點資訊 -->
        <div
          class="bg-white p-4 rounded-lg shadow-md border border-gray-200 w-1/2 mr-4 text-sm space-y-2"
        >
          <p class="font-bold text-[#286047]">
            目前選播捷運站：<span class="text-red-500">公館</span>
          </p>
          <p class="text-gray-700">知名景點：國立臺灣大學、水源市場 (抓取資料中...)</p>
        </div>

        <!-- 右下方：天氣與降雨資訊 -->
        <div
          class="bg-white p-4 rounded-lg shadow-md border border-gray-200 w-1/3 text-sm space-y-2"
        >
          <p class="text-gray-700">天氣：(抓取天氣API資料)</p>
          <p class="text-gray-700">降雨機率：(抓取天氣API資料)</p>
        </div>
      </div>

      <!-- 右下角：聊天室按鈕 (絕對定位，使用設計稿中的紅色) -->
      <!-- <button
        class="absolute bottom-6 right-6 px-8 py-3 bg-red-500 text-white font-extrabold text-lg rounded-full shadow-xl hover:bg-red-600 transition duration-300 transform hover:scale-105"
      >
        聊 天 室
      </button> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import IntroCard from '@/components/cards/IntroCard.vue'
import { ref } from 'vue'

// 模擬介紹卡片的內容
const introContents = ref([
  'STEP 1: 選擇捷運站\n選擇松山新店線(綠線)想探索的捷運站。',
  'STEP 2: 確認目的\n1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
  'STEP 3: 發送邀約 / 選擇邀約\n此部分將根據 邀約發送方 or 邀約選擇方 而有不同操作方式。',
  'STEP 4: 填寫滿意度\n完成邀約後，系統會引導您填寫本次體驗的滿意度，以便優化配對服務。',
  'STEP 5: 成功配對\n當雙方確認並完成所有步驟後，恭喜您！邀約成功，準備出發吧！',
])
</script>

<style scoped>
/* 確保左側滾動條有樣式，模擬設計稿的視覺效果 */
.intro-cards-scroll-area::-webkit-scrollbar {
  width: 8px;
}
.intro-cards-scroll-area::-webkit-scrollbar-thumb {
  background-color: #a5d6a7; /* 淺綠色 light green */
  border-radius: 4px;
}
.intro-cards-scroll-area::-webkit-scrollbar-track {
  background: #f3f4f6; /* 淺灰 */
}
</style>
