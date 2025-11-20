import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useLoadingStore } from '@/stores/modules/loading'
import { useRoleStore } from '@/stores/modules/useRole'

// --- Layouts & Views ---
const WebLayout = () => import('@/views/web.vue')
const BCMSLogin = () => import('@/views/bcms/login.vue')

const HomePage = () => import('@/views/web/index.vue')
const AboutPage = () => import('@/views/web/about.vue')

const SenderView = () => import('@/views/web/SenderView.vue')
const ReceiverView = () => import('@/views/web/ReceiverView.vue')

const HistoryPage = () => import('@/views/web/history.vue')
const ProfilePage = () => import('@/views/web/profile.vue')

const NotFound = () => import('@/views/404.vue')

export const webRouteName = 'web'

// --- Route Definitions ---

export const publicWebRoutes: RouteRecordRaw[] = [
  {
    path: '',
    name: 'home',
    component: HomePage,
    meta: {
      title: '首頁',
      isPublic: true,
      requiresAuth: false,
    },
  },
  {
    path: 'invite/sender/:stationKey',
    name: 'SenderView',
    component: SenderView,
    props: true,
    meta: {
      title: '發送邀約',
      isPublic: true,
      requiresAuth: false,
    },
  },
  {
    path: 'invite/receiver/:stationKey',
    name: 'ReceiverView',
    component: ReceiverView,
    props: true,
    meta: {
      title: '探索活動',
      isPublic: true,
      requiresAuth: false,
    },
  },
  {
    path: 'about',
    name: 'About',
    component: AboutPage,
    meta: {
      title: '關於我們',
      isPublic: true,
      requiresAuth: false,
    },
  },
]

export const privateWebRoutes: RouteRecordRaw[] = [
  {
    path: 'history',
    name: 'History',
    component: HistoryPage,
    meta: {
      title: '邀約歷史',
      isPublic: false,
      requiresAuth: true,
    },
  },
  {
    path: 'profile',
    name: 'Profile',
    component: ProfilePage,
    meta: {
      title: '帳戶資料',
      isPublic: false,
      requiresAuth: true,
    },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/bcms',
      children: [
        {
          path: 'login',
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
      children: [...publicWebRoutes, ...privateWebRoutes],
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

// --- Navigation Guards (整合您提供的邏輯) ---

router.beforeEach((to, from, next) => {
  const loadingStore = useLoadingStore()
  const roleStore = useRoleStore()

  // 開啟 Loading
  loadingStore.setLoading(true, '載入中...')

  const requiresAuth = to.meta.requiresAuth
  // 判斷是否登入：如果身分不是 'guest'，就視為已登入 (user 或 admin)
  const isLoggedIn = !roleStore.isGuest

  if (requiresAuth && !isLoggedIn) {
    // 1. 需要登入但未登入 -> 導向登入頁 (帶上 redirect 參數)
    console.warn('[Router] Access denied. Redirecting to login.', to.fullPath)
    next({ name: 'BCMSLogin', query: { redirect: to.fullPath } })
    // 因為被導走了，這裡要手動關閉 loading (或者依靠 afterEach，但保險起見先關)
    loadingStore.setLoading(false)
  } else if (to.name === 'BCMSLogin' && isLoggedIn) {
    // 2. 已登入卻想去登入頁 -> 導向首頁 (避免重複登入)
    next({ name: 'home' })
    loadingStore.setLoading(false)
  } else {
    // 3. 通行
    next()
  }
})

router.afterEach((to) => {
  const loadingStore = useLoadingStore()

  // 延遲關閉 Loading 以呈現轉場效果
  setTimeout(() => {
    loadingStore.setLoading(false)
  }, 300)

  // 設定網頁標題
  const defaultTitle = 'Meetro - 相遇地圖'
  document.title = (to.meta.title ? to.meta.title + ' | ' : '') + defaultTitle
})

export default router
