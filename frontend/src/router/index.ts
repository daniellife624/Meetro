import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useLoadingStore } from '@/stores/modules/loading' // 導入載入 Store
// import { useAuthStore } from '@/stores/modules/auth' // 假設您有一個 Auth Store

// =======================================================
// 1. 公開/私有元件載入 (Public & Private Component Imports)
// 根據您的專案結構，元件路徑應如下：
// =======================================================

const WebLayout = () => import('@/views/web.vue') // 網站主要佈局 (根據截圖，應為 /views/web/web.vue 或 /views/web.vue)
const BCMSLogin = () => import('@/views/bcms/login.vue')

// 公開 Web 頁面 (Public Web Pages)
const HomePage = () => import('@/views/web/index.vue') // 假設 /web/index.vue 是首頁
const AboutPage = () => import('@/views/web/about.vue')

// 私有 Web 頁面 (Private/Protected Web Pages - 登入後可見)
const HistoryPage = () => import('@/views/web/history.vue') // 邀約歷史
const ProfilePage = () => import('@/views/web/profile.vue') // 帳戶資料

// 載入 404 頁面
const NotFound = () => import('@/views/404.vue')

/**
 * @description 導出 Web Layout 的根路由名稱。
 * @const
 */
export const webRouteName = 'web'

// =======================================================
// 2. 路由定義 (Route Definitions)
// =======================================================

/**
 * @description 根據傳入的子路由列表，建立完整的 Web Layout 父級路由物件。
 * 這個函式用於 Pinia Store 中動態新增特定角色的路由。
 * @param children 傳入特定角色的子路由列表
 * @returns 完整的 web 父級路由物件
 */
export const getWebRoute = (children: RouteRecordRaw[]): RouteRecordRaw => ({
  path: '/web',
  name: webRouteName,
  component: WebLayout, // 網站佈局元件
  children,
})

/**
 * @description 應用程式啟動時必須立即存在的公共 Web 子路由列表。
 * @const
 */
export const publicWebRoutes: RouteRecordRaw[] = [
  {
    path: '', // 完整路徑: /web
    name: 'home',
    component: HomePage,
    meta: {
      title: '首頁',
      isPublic: true,
      requiresAuth: false,
    },
  },
  {
    path: 'about', // 完整路徑: /web/about
    name: 'About',
    component: AboutPage,
    meta: {
      title: '關於我們',
      isPublic: true,
      requiresAuth: false,
    },
  },
]

/**
 * @description 登入後需要動態新增的私有 Web 子路由列表。
 * 這些路徑將在用戶成功登入後，使用 router.addRoute() 添加到 'web' 父級路由。
 * @const
 */
export const privateWebRoutes: RouteRecordRaw[] = [
  {
    path: 'history', // 完整路徑: /web/history
    name: 'History',
    component: HistoryPage,
    meta: {
      title: '邀約歷史',
      isPublic: false, // 必須登入
      requiresAuth: true,
    },
  },
  {
    path: 'profile', // 完整路徑: /web/profile
    name: 'Profile',
    component: ProfilePage,
    meta: {
      title: '帳戶資料',
      isPublic: false, // 必須登入
      requiresAuth: true,
    },
  },
]

// =======================================================
// 3. 路由實例化 (Router Instantiation)
// =======================================================

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/bcms',
      // component: BCMSLayout, // 假設後臺佈局存在
      children: [
        {
          path: 'login', // /bcms/login
          name: 'BCMSLogin',
          component: BCMSLogin,
          meta: {
            title: '後臺登入',
            isPublic: true,
            requiresAuth: false,
          },
        },
      ],
    },

    {
      path: '/web',
      name: webRouteName,
      component: WebLayout,
      children: publicWebRoutes,
    },

    {
      path: '/',
      redirect: { name: 'home' },
    },

    {
      path: '/:catchAll(.*)',
      name: 'NotFound',
      component: NotFound,
      meta: { title: '頁面不存在' },
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  },
})

// =======================================================
// 4. 路由守衛 (Navigation Guards) - 核心權限檢查區
// =======================================================

// router.beforeEach((to, from, next) => {
//   const loadingStore = useLoadingStore()
//   loadingStore.setLoading(true, '正在切換頁面...')

//   // 假設 useAuthStore 存在且包含 isUserLoggedIn 狀態
//   // const authStore = useAuthStore()
//   // const isLoggedIn = authStore.isLoggedIn // 替換為實際的登入狀態檢查

//   const requiresAuth = to.meta.requiresAuth
//   const isLoggedIn = isUserLoggedInStub() // 使用暫存函式檢查登入狀態

//   if (requiresAuth && !isLoggedIn) {
//     // 檢查 1：如果路由需要登入 (requiresAuth: true) 且用戶未登入
//     console.warn('Need login to access:', to.fullPath)
//     // 導向登入頁面，並帶上原本的目標路徑作為查詢參數 (redirect query)
//     next({ name: 'BCMSLogin', query: { redirect: to.fullPath } })
//     loadingStore.setLoading(false) // 停止載入指示
//   } else if (!requiresAuth && isLoggedIn && to.name === 'BCMSLogin') {
//     // 檢查 2：如果用戶已登入，但試圖存取登入頁面
//     next({ name: 'Profile' }) // 導向到登入後的第一個私有頁面
//     loadingStore.setLoading(false) // 停止載入指示
//   } else {
//     // 檢查 3：通過所有檢查，或存取公共頁面
//     next()
//   }
// })

// router.afterEach((to, from) => {
//   const loadingStore = useLoadingStore()

//   setTimeout(() => {
//     loadingStore.setLoading(false)
//   }, 300)

//   const defaultTitle = 'Meetro App'
//   document.title = (to.meta.title ? to.meta.title + ' | ' : '') + defaultTitle
// })

/**
 * @description 假定判斷用戶是否登入的函式。
 * 實際應用中應檢查 Pinia Store (e.g., useAuthStore().isLoggedIn)。
 * @returns {boolean}
 */
function isUserLoggedInStub(): boolean {
  // TODO: 請替換為您的實際 Pinia/Auth 登入狀態檢查邏輯
  return false
}

export default router
