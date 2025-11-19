import { RouteRecordRaw } from 'vue-router'
// 假設您的 HomeView.vue 在 src/views/web/ 或 src/views/
// 根據您的檔案結構 (image_7896fd.png)，它看起來在 src/views/ 下
import HomeView from '@/views/HomeView.vue'
import NotFound from '@/views/404.vue' // 假設 404.vue 也在 src/views/ 下

/**
 * 基礎常量路由 (Constant Routes)
 * 這些路由在應用程式啟動時就被註冊，不需要權限即可訪問。
 * 必須包含 home, login, 404 等基礎路由，以避免啟動時的 'No match for home' 錯誤。
 */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home', // ⭐️ 關鍵修正：明確定義 'home' 名稱
    component: HomeView,
    meta: { title: '首頁', requiresAuth: false },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/web/login.vue'), // 假設登入頁面在 src/views/web/login.vue
    meta: { title: '登入', requiresAuth: false },
  },
]

/**
 * 錯誤處理路由 (Error Route)
 * 必須放在路由表的最後，用於捕獲所有未匹配的路徑。
 */
export const errorRoute: RouteRecordRaw = {
  path: '/:pathMatch(.*)*',
  name: 'NotFound',
  component: NotFound,
  meta: { title: '404 找不到頁面' },
}
