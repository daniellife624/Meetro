import { RouteRecordRaw } from 'vue-router'

// 這是為了解決構建錯誤而創建的 BCMS 路由模組佔位符。

// 定義 BCMS 基礎路由
export const BCMSRoute: RouteRecordRaw = {
  path: '/bcms',
  name: 'bcms',
  // 注意：這裡假設後台管理系統會有一個主要的佈局組件
  component: () => import('@/views/bcms/BCMSLayout.vue').catch(() => null),
  meta: {
    title: 'Meetro 後台管理系統',
    requiresAuth: true, // 假設需要認證
  },
  children: [
    // 這裡可以放置所有 BCMS 內部頁面的路由
    {
      path: 'dashboard',
      name: 'bcms-dashboard',
      component: () => import('@/views/bcms/Dashboard.vue').catch(() => null),
      meta: {
        title: '儀表板',
      },
    },
  ],
}

// 為了讓編譯成功，我們需要確保 BCMSLayout.vue 和 Dashboard.vue 檔案存在。
// 如果它們不存在，請先創建最小化的佔位符檔案。

// 為了避免編譯錯誤，我們現在也創建 BCMSLayout.vue 和 Dashboard.vue 的最小佔位符。
// 注意：由於您在 `router/index.ts` 中已經有 `/bcms/login`，
// 這個 BCMSLayout.vue 檔案是所有 BCMS 內部頁面所需的父組件。
