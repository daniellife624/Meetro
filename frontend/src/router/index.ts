import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useLoadingStore } from '@/stores/modules/loading'
import { useRoleStore } from '@/stores/modules/useRole'

// --- Layouts ---
const WebLayout = () => import('@/views/web.vue')

// --- Views: BCMS (後台) ---
const BCMSLogin = () => import('@/views/bcms/login.vue') // 後台登入 (獨立頁面)
const BCMSDashboard = () => import('@/views/bcms/index.vue') // 後台儀表板

// --- Views: Web (前台) ---
const WebLogin = () => import('@/views/web/login.vue')
const WebRegister = () => import('@/views/web/register.vue')
const HomePage = () => import('@/views/web/index.vue')
const AboutPage = () => import('@/views/web/about.vue')
const SenderView = () => import('@/views/web/SenderView.vue')
const ReceiverView = () => import('@/views/web/ReceiverView.vue')
const HistoryPage = () => import('@/views/web/history.vue')
const ProfilePage = () => import('@/views/web/profile.vue')
const EmaWallView = () => import('@/views/web/EmaWallView.vue')
const NotFound = () => import('@/views/404.vue')

export const webRouteName = 'web'

// --- Route Definitions ---

export const publicWebRoutes: RouteRecordRaw[] = [
  {
    path: '',
    name: 'home',
    component: HomePage,
    meta: { title: '首頁', isPublic: true, requiresAuth: false },
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
    meta: { title: '發送邀約', isPublic: true, requiresAuth: false },
  },
  {
    path: 'invite/receiver/:stationKey',
    name: 'ReceiverView',
    component: ReceiverView,
    props: true,
    meta: { title: '探索活動', isPublic: true, requiresAuth: false },
  },
  {
    path: 'about',
    name: 'About',
    component: AboutPage,
    meta: { title: '關於我們', isPublic: true, requiresAuth: false },
  },
  {
    path: 'ema/:stationKey',
    name: 'EmaWall',
    component: EmaWallView,
    props: true,
    meta: { title: '站點繪馬牆', isPublic: true, requiresAuth: false },
  },
]

export const privateWebRoutes: RouteRecordRaw[] = [
  {
    path: 'history',
    name: 'History',
    component: HistoryPage,
    meta: { title: '邀約歷史', isPublic: false, requiresAuth: true },
  },
  {
    path: 'profile',
    name: 'Profile',
    component: ProfilePage,
    meta: { title: '帳戶資料', isPublic: false, requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 1. 後台登入 (獨立路由)
    {
      path: '/bcms/login',
      name: 'BCMSLogin',
      component: BCMSLogin,
      meta: { title: '後臺登入', isPublic: true, requiresAuth: false },
    },

    // 2. 後台管理區
    {
      path: '/bcms',
      component: WebLayout,
      redirect: { name: 'BCMSDashboard' },
      children: [
        {
          path: 'dashboard',
          name: 'BCMSDashboard',
          component: BCMSDashboard,
          meta: { title: '後臺儀表板', isPublic: false, requiresAuth: true },
        },
      ],
    },

    // 3. 前台網頁
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
    if (savedPosition) return savedPosition
    return { top: 0, behavior: 'smooth' }
  },
})

// --- Navigation Guards ---

router.beforeEach((to, from, next) => {
  const loadingStore = useLoadingStore()
  const roleStore = useRoleStore()

  loadingStore.setLoading(true, '載入中...')

  const requiresAuth = to.meta.requiresAuth
  const isLoggedIn = !roleStore.isGuest

  const isAuthPage = ['WebLogin', 'WebRegister', 'BCMSLogin'].includes(to.name as string)

  if (requiresAuth && !isLoggedIn) {
    // 1. 需登入但未登入
    console.warn('[Router] Access denied.', to.fullPath)
    if (to.path.startsWith('/bcms')) {
      next({ name: 'BCMSLogin', query: { redirect: to.fullPath } })
    } else {
      next({ name: 'WebLogin', query: { redirect: to.fullPath } })
    }
    loadingStore.setLoading(false)
  } else if (isAuthPage && isLoggedIn) {
    // 2. 已登入卻想去登入頁 (防呆)
    console.warn('[Router] Already logged in. Redirecting.')
    if (roleStore.isAdmin) {
      next({ name: 'BCMSDashboard' })
    } else {
      next({ name: 'home' })
    }
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
  const defaultTitle = to.path.startsWith('/bcms') ? 'Meetro 後台管理' : 'Meetro - 相遇地圖'
  document.title = (to.meta.title ? to.meta.title + ' | ' : '') + defaultTitle
})

export default router
