import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useLoadingStore } from '@/stores/modules/loading'
import { useRoleStore } from '@/stores/modules/useRole'

// --- Layouts & Views ---
const WebLayout = () => import('@/views/web.vue')
const BCMSLogin = () => import('@/views/bcms/login.vue') // 後台登入

// 前台使用者認證頁面
const WebLogin = () => import('@/views/web/login.vue')
const WebRegister = () => import('@/views/web/register.vue')

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
    path: 'login',
    name: 'WebLogin',
    component: WebLogin,
    meta: { title: '會員登入', isPublic: true, requiresAuth: false },
  },
  {
    path: 'register',
    name: 'WebRegister',
    component: WebRegister,
    meta: { title: '會員註冊', isPublic: true, requiresAuth: false },
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

// --- Navigation Guards ---

router.beforeEach((to, from, next) => {
  const loadingStore = useLoadingStore()
  const roleStore = useRoleStore()

  loadingStore.setLoading(true, '載入中...')

  const requiresAuth = to.meta.requiresAuth
  // 判斷是否登入：如果身分不是 'guest'，就視為已登入 (user 或 admin)
  const isLoggedIn = !roleStore.isGuest

  // 定義哪些頁面是「登入後不應該再看到」的 (登入、註冊、後台登入)
  const isAuthPage = ['WebLogin', 'WebRegister', 'BCMSLogin'].includes(to.name as string)

  if (requiresAuth && !isLoggedIn) {
    // 1. 需要登入但未登入 -> 導向使用者登入頁 (WebLogin)
    console.warn('[Router] Access denied. Redirecting to WebLogin.', to.fullPath)
    next({ name: 'WebLogin', query: { redirect: to.fullPath } })
    loadingStore.setLoading(false)
  } else if (isAuthPage && isLoggedIn) {
    // 2. 已登入卻想去 登入/註冊 頁面 -> 導向首頁 (避免重複登入)
    console.warn('[Router] Already logged in. Redirecting to home.')
    next({ name: 'home' })
    loadingStore.setLoading(false)
  } else {
    // 3. 通行
    next()
  }
})

router.afterEach((to) => {
  const loadingStore = useLoadingStore()
  setTimeout(() => {
    loadingStore.setLoading(false)
  }, 300)
  const defaultTitle = 'Meetro - 相遇地圖'
  document.title = (to.meta.title ? to.meta.title + ' | ' : '') + defaultTitle
})

export default router
