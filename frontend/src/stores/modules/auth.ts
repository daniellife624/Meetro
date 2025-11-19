import { defineStore } from 'pinia'
import { ref } from 'vue'
// 修正：導入 publicWebRoutes，這是目前我們定義的公開 Web 子路由
import router, { getWebRoute, publicWebRoutes, webRouteName, type RouteRecordRaw } from '@/router'

// 模擬需要動態新增的**受保護**路由
// 這些路由只有在用戶登入後才需要被添加到 WebLayout 中。
const dynamicProtectedRoutes: RouteRecordRaw[] = [
  // 範例：只有登入用戶才能訪問的會員中心頁面 (目前為空，等待未來定義)
  // {
  //   path: 'member',
  //   name: 'MemberCenter',
  //   component: () => import('@/views/web/member.vue'),
  //   meta: { title: '會員中心', requiresAuth: true },
  // },
]

export const useAuthStore = defineStore('auth', () => {
  // 模擬登入狀態，預設為未登入
  const isUserLoggedIn = ref(false) // 模擬使用者角色 (用於 useRole 判斷)

  const role = ref<'user' | null>(null)

  function login() {
    isUserLoggedIn.value = true
    role.value = 'user'
    console.log('User logged in.')
  }

  function logout() {
    isUserLoggedIn.value = false
    role.value = null
    console.log('User logged out.')
  } /**
   * @description 負責檢查登入狀態、動態新增路由並處理初次導航。
   * 這個方法必須在 main.ts 中被 await 調用。
   */

  async function initApp() {
    // 1. 模擬非同步初始化檢查 (例如：檢查 Token, 獲取使用者資訊)
    console.log('AuthStore: 模擬非同步初始化中...')
    await new Promise((resolve) => setTimeout(resolve, 50)) // 模擬延遲 50ms
    // 2. 獲取當前路由 (在添加路由之前)

    const currentPath = router.currentRoute.value.fullPath // 3. 根據角色動態新增路由

    const routesToDynamicallyAdd = dynamicProtectedRoutes
    routesToDynamicallyAdd.forEach((childRoute) => {
      // 檢查子路由是否存在，不存在則新增
      if (!router.hasRoute(childRoute.name!)) {
        // 將受保護路由新增為 Web Layout 的子路由
        router.addRoute(webRouteName, childRoute)
        console.log(`AuthStore: 動態新增路由 ${String(childRoute.name)}。`)
      }
    }) // 4. 處理首次導航
    if (currentPath === '/' || currentPath === '/web') {
      // 導航到靜態定義的首頁 'home'
      await router.replace({ name: 'home' }).catch((err) => {
        // 捕獲並忽略導航錯誤
        if (err.name !== 'NavigationDuplicated' && !err.message.includes('redundant navigation')) {
          throw err
        }
      })
      console.log('AuthStore: 首次導航完成，替換為 home 路由。')
    } else {
      // 如果用戶嘗試訪問其他路徑，則讓它繼續導航（所有靜態路由和動態路由已就緒）
      console.log(`AuthStore: 繼續導航到 ${currentPath}。`)
    }
  }

  return {
    isUserLoggedIn,
    role,
    login,
    logout,
    initApp, // 匯出供 main.ts 使用
  }
})
