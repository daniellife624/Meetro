<template>
  <svg
    :class="`w-${size} h-${size}`"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <!-- Send Icon (用於 ExploreStationPopup.vue) -->
    <template v-if="name === 'send'">
      <line x1="22" y1="2" x2="11" y2="13"></line>
      <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
    </template>

    <!-- Users Icon (用於 ExploreStationPopup.vue) -->
    <template v-if="name === 'users'">
      <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
      <circle cx="8.5" cy="7" r="4"></circle>
      <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
    </template>

    <!-- Check Icon (用於 ExploreStationPopup.vue) -->
    <template v-if="name === 'check'">
      <polyline points="20 6 9 17 4 12"></polyline>
    </template>

    <!-- X Icon (用於 PopupBoxLayout.vue) -->
    <template v-if="name === 'x'">
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </template>

    <!-- Star Icon (用於 SenderView.vue) -->
    <template v-if="name === 'star'">
      <polygon
        points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
      ></polygon>
    </template>

    <!-- Clock Icon (用於 SenderView.vue) -->
    <template v-if="name === 'clock'">
      <circle cx="12" cy="12" r="10"></circle>
      <polyline points="12 6 12 12 16 14"></polyline>
    </template>

    <!-- Map-Marker-Alt Icon (用於 SenderView.vue - 模擬 Location Pin) -->
    <template v-if="name === 'location-dot'">
      <!-- 模擬一個地點標記圖案 (使用 map-pin) -->
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
      <circle cx="12" cy="10" r="3"></circle>
    </template>

    <!-- Map-Marker-Alt Icon for Placeholder (用於 SenderView.vue - 模擬地圖上的標記) -->
    <template v-if="name === 'map-marker-alt'">
      <!-- 使用一個簡單的標記 SVG -->
      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"></path>
      <circle cx="12" cy="9" r="2.5"></circle>
    </template>
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  name: 'send' | 'users' | 'check' | 'x' | 'star' | 'clock' | 'location-dot' | 'map-marker-alt' // 圖示名稱
  size?: string // Tailwind class size (e.g. '4', '6', '8', 應為 w-X h-X)
  // color?: string; // 顏色由父組件的 Tailwind class 決定
}>()

// 將 size 轉換為 Tailwind class 接受的字串
const size = computed(() => props.size || '6')
</script>

<style scoped>
/* 這裡不需要特別的 scoped 樣式 */
</style>
