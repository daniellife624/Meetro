import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useLoadingStore } from '@/stores/modules/loading'

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

export const getWebRoute = (children: RouteRecordRaw[]): RouteRecordRaw => ({
  path: '/web',
  name: webRouteName,
  component: WebLayout,
  children,
})

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

// router.beforeEach((to, from, next) => {
//   const loadingStore = useLoadingStore()
//   loadingStore.setLoading(true, '正在切換頁面...')

//   const requiresAuth = to.meta.requiresAuth
//   const isLoggedIn = isUserLoggedInStub()

//   if (requiresAuth && !isLoggedIn) {
//     console.warn('Need login to access:', to.fullPath)
//     next({ name: 'BCMSLogin', query: { redirect: to.fullPath } })
//     loadingStore.setLoading(false)
//   } else if (!requiresAuth && isLoggedIn && to.name === 'BCMSLogin') {
//     next({ name: 'Profile' })
//     loadingStore.setLoading(false)
//   } else {
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

// function isUserLoggedInStub(): boolean {
//   return false
// }

export default router
