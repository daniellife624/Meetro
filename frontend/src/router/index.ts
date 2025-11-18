// 使用 @/ 別名來修正所有本地模組的路徑解析錯誤，並明確指定檔案擴展名 (.ts)

// 🚨 修正路徑：將 store (單數) 修正為 stores (複數)
import { useLoadingStore } from '@/stores/modules/loading.ts'

// 修正所有本地模組的導入，全部使用 @/ 絕對路徑 + 顯式擴展名
import { BCMSRoute } from '@/router/modules/bcms/index.ts'
import { notFoundRoute } from '@/router/modules/404.ts'
import { getWebRoute } from '@/router/modules/index.ts'
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { allRoutes } from '@/router/modules/AllRoutes.ts'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/bcms/login',
    name: 'bcms-login',
    component: () => import('@/views/bcms/login.vue'),
    meta: {
      title: 'Meetro 後台管理系統 - 登入',
    },
  },
  BCMSRoute,
  getWebRoute(allRoutes),
  //404
  notFoundRoute,
]

const router = createRouter({
  // 注意：在 Vite 專案中，使用 import.meta.env.BASE_URL 而非 process.env.BASE_URL
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from) => {
  const { title, mainClass } = to.meta
  document.title = title || 'Meetro'
  const loadingStore = useLoadingStore()
  // 注意：這裡將 loadingStore.isLoading = true 改為呼叫 action
  if (to.path !== from.path) loadingStore.startLoading('路由切換中...')
})

router.beforeResolve((to, from) => {
  if (to.path !== from.path) document.documentElement.scrollTo({ top: 0, left: 0 })
})

router.afterEach(() => {
  const loadingStore = useLoadingStore()
  // 注意：這裡將 loadingStore.isLoading = false 改為呼叫 action
  loadingStore.stopLoading()
})

export default router
