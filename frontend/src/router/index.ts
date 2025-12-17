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
// const AboutPage = () => import('@/views/web/about.vue')
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
  // {
  //   path: 'about',
  //   name: 'About',
  //   component: AboutPage,
  //   meta: { title: '關於我們', isPublic: true, requiresAuth: false },
  // },
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
    // 後台登入 (獨立路由)
    {
      path: '/bcms/login',
      name: 'BCMSLogin',
      component: BCMSLogin,
      meta: { title: '後臺登入', isPublic: true, requiresAuth: false },
    },

    // 後台管理區
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

    // 前台網頁
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
const timeoutPromise = (ms: number, promise: Promise<any>) => {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      reject(new Error('API Timeout: Role fetching exceeded 5 seconds.'))
    }, ms)

    promise.then(
      (res) => {
        clearTimeout(timer)
        resolve(res)
      },
      (err) => {
        clearTimeout(timer)
        reject(err)
      },
    )
  })
}

router.beforeEach(async (to, from, next) => {
  const loadingStore = useLoadingStore()
  const roleStore = useRoleStore()

  // 確保載入狀態
  loadingStore.setLoading(true, '載入中...')
  const isLoggedIn = roleStore.isAuthenticated
  const isAdmin = roleStore.isAdmin
  const isLoginPath = to.name === 'WebLogin'

  // ----------------------------------------------------
  // 核心邏輯
  // ----------------------------------------------------

  if (to.name === 'BCMSDashboard') {
    // 1. 導航到 /web/bcms (Dashboard)
    if (!isAdmin) {
      // 不是 Admin，無權限，導回首頁
      console.warn('[Router] BCMS Access Denied. Redirecting to Home.')
      return next({ name: 'home' })
    }
    // 是 Admin，允許通行
    return next()
  }

  if (isLoginPath) {
    // 2. 導航到 /web/login 頁面
    if (isLoggedIn) {
      // 已登入者 (Admin 或 User) 訪問登入頁
      console.warn('[Router] Already Logged In. Redirecting.')

      if (isAdmin) {
        // 如果是 Admin，導向 BCMS
        return next({ name: 'BCMSDashboard' })
      } else {
        // 如果是普通 User，導向 Home
        return next({ name: 'home' })
      }
    }
    // 未登入，允許進入登入頁
    return next()
  }

  // 3. 所有其他頁面 (Home, Profile, History, etc.)

  // 確保所有 requiresAuth 的頁面能被保護 (例如 Profile/History)
  if (to.meta.requiresAuth && !isLoggedIn) {
    console.warn('[Router] Protected Page Access Denied. Redirect to WebLogin.')
    return next({ name: 'WebLogin', query: { redirect: to.fullPath } })
  }

  // 4. 允許通行
  next()
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
