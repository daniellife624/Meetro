// src/router/index.ts - 專門負責定義和匯出 router 實例

import { createRouter, createWebHistory } from 'vue-router'
import { useLoadingStore } from '@/stores/modules/loading' // 導入載入 Store

// 載入佈局元件 (Layouts)
// const WebLayout = () => import('@/layouts/WebLayout.vue')
// const BCMSLayout = () => import('@/layouts/BCMSLayout.vue')

// 載入公用頁面 (Web Pages)
const WebIndex = () => import('@/views/web/index.vue')
// const WebAbout = () => import('@/views/web/about.vue') // 假設有其他頁面

// 載入後臺頁面 (BCMS Pages)
const BCMSLogin = () => import('@/views/bcms/login.vue')
// const BCMSDashboard = () => import('@/views/bcms/dashboard.vue')

const router = createRouter({
  // 使用 HTML5 History 模式
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // =======================================================
    // 1. 公開網站 (Web Layout) 路由
    // =======================================================
    {
      path: '/', // 這是 Web Layout 的基礎路徑
      // component: WebLayout,
      children: [
        {
          path: '', // 🌟 關鍵點：空的 path '' 會繼承父級的 '/'，所以完整的路徑就是 '/'
          name: 'Home',
          component: WebIndex, // 對應到您正在設計的 index.vue
          meta: { title: 'Meetro - 首頁' },
        },
        // {
        //   path: 'about',
        //   name: 'About',
        //   component: WebAbout,
        //   meta: { title: '關於我們' },
        // },
      ],
    },

    // =======================================================
    // 2. 後臺管理系統 (BCMS Layout) 路由
    // =======================================================
    {
      path: '/bcms',
      // component: BCMSLayout,
      children: [
        {
          path: 'login', // 完整的路徑為 /bcms/login
          name: 'BCMSLogin',
          component: BCMSLogin,
          meta: {
            title: '後臺登入',
            isPublic: true, // 標記為公開頁面，不需要驗證
          },
        },
        // {
        //   path: 'dashboard', // 完整的路徑為 /bcms/dashboard
        //   name: 'BCMSDashboard',
        //   component: BCMSDashboard,
        //   meta: {
        //     title: '儀表板',
        //     requiresAuth: true, // 標記為需要驗證
        //   },
        // },
      ],
    },

    // =======================================================
    // 3. 404 頁面
    // =======================================================
    {
      path: '/:catchAll(.*)',
      name: 'NotFound',
      // component: () => import('@/views/shared/NotFound.vue'),
      meta: { title: '頁面不存在' },
    },
  ],
  // 滾動行為
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  },
})

// 路由前置守衛 (Navigation Guards) - 用於顯示載入動畫和處理權限
router.beforeEach((to, from, next) => {
  const loadingStore = useLoadingStore()
  // 1. 顯示載入遮罩
  // loadingStore.setLoading(true, '正在切換頁面...')

  // 2. 處理權限（範例）
  // 這裡可以加入檢查 `to.meta.requiresAuth` 的邏輯，如果使用者未登入則導向登入頁。

  // 3. 繼續導航
  next()
})

router.afterEach((to, from) => {
  const loadingStore = useLoadingStore()
  // 1. 隱藏載入遮罩
  // 為了確保載入動畫能被看到，這裡加入一個短暫的延遲
  setTimeout(() => {
    // loadingStore.setLoading(false)
  }, 300)

  // 2. 更新頁面標題
  const defaultTitle = 'Meetro App'
  document.title = (to.meta.title ? to.meta.title + ' | ' : '') + defaultTitle
})

export default router
