// frontend/src/router/modules/user.ts
import type { RouteRecordRaw } from 'vue-router'

// 假設這裡定義了用戶相關和主要頁面的路由，並使用 export default 匯出
const userRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home', // 確保這裡有 'home' 路由名稱，以解決 "No match" 錯誤
    component: () => import('@/views/HomeView.vue'), // 假設 HomeView.vue 存在
    meta: {
      title: '首頁',
      requiresAuth: false,
    },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/web/about.vue'),
    meta: {
      title: '關於我們',
      requiresAuth: false,
    },
  },
  // 可以在這裡加入更多用戶相關的路由
]

// 使用 default export 來解決 "does not provide an export named 'default'" 錯誤
export default userRoutes
