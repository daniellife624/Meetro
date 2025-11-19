import router from '@/router'
import beforeLoginRoutes from '@/router/modules/BeforeLogin'
import userRoutes from '@/router/modules/user'
import useBCMSStore from './bcms'
// 由於 useCookies 暫時使用 Stub 且不再依賴外部庫，這裡的匯入路徑是正確的
import useCookies from '@/composables/useCookies'

import { UserAuth } from '../api/types/auth'
import { getNavList } from './../composables/useNav'
import { NavItem } from './../types/header/index.d'
// import { getWebRoute, webRouteName } from './../router/modules/index'
// import { notFoundRouteName, notFoundRoute } from './../router/modules/404'
import { getWebRoute, webRouteName } from '@/router'
import { defineStore } from 'pinia'
import { ApiRole, WebRole } from '@/types/web'
import { Router } from 'vue-router'

export interface State {
  isLogin: boolean
  isInit: boolean
  userAuth: UserAuth | null //使否正在使用後台管理系統
  usingBCMS: boolean
}
export const useStore = defineStore('main', {
  state: (): State => ({
    isLogin: false,
    isInit: false,
    userAuth: null,
    usingBCMS: false,
  }),
  actions: {
    /**
     * 驗證是否登入
     */
    auth() {
      // *** 暫時移除 Cookie 讀取邏輯，確保應用程式啟動 ***
      this.updateUserAuth({
        token: '', // 原為 this.$cookies.token.get(), 暫時給空字串
        roleId: 0, // 原為 this.$cookies.roleId.get(), 暫時給 0
      })
      return this.initRoute()
    },
    initRoute() {
      this.isInit = true // this.initNav();
      const role = this.role // 移除404
      router.removeRoute(notFoundRouteName) //移除web
      router.removeRoute(webRouteName)
      if (!role) {
        //未登入
        const webRoute = getWebRoute(beforeLoginRoutes)
        router.addRoute(webRoute)
      } else {
        //已登入
        const routes = {
          user: userRoutes,
        }[role]
        const webRoute = getWebRoute(routes)
        router.addRoute(webRoute)
      }

      router.addRoute(notFoundRoute)
      return router
    } /**
     * 初始化header 導航
     */, // initNav() {
    //   const role = this.role;
    //   if (!role) {
    //     this.nav = getNavList(null);
    //     return;
    //   }
    //   this.nav = getNavList(role);
    // },
    updateUserAuth(userAuth: UserAuth = { token: '', roleId: 0 }, remember: boolean = true) {
      const { token, roleId } = userAuth
      const cookies = this.$cookies
      if (!token || !roleId) {
        this.isLogin = false
        this.userAuth = null
        this.isLogin = false // cookies.removeAll() // <-- 暫時註解掉 Cookie 操作
        return
      }

      this.userAuth = {
        token,
        roleId,
      } // cookies.token.set(token, remember) // <-- 暫時註解掉 Cookie 操作
      // cookies.roleId.set(roleId, remember) // <-- 暫時註解掉 Cookie 操作
      this.isLogin = true
    },
  },
  getters: {
    nav(): NavItem[] {
      const role = this.role
      if (!role) return getNavList(null)

      return getNavList(role)
    },
    navGrouped(): NavItem[] {
      const role = this.role
      if (!role) return getNavList(null, true)

      return getNavList(role, true)
    },
    $cookies: () => {
      // 繼續使用 useCookies Stub，因為它的函數已被更新為不依賴外部庫
      const cookies = useCookies()
      return {
        removeAll: () => {
          cookies.remove('token')
          cookies.remove('roleId')
        },
        token: {
          get: () => cookies.get('token') || '',
          set: (value: string, remember: boolean) => cookies.set('token', value, remember),
          remove: () => cookies.remove('token'),
        },
        roleId: {
          get: () => parseInt(cookies.get('roleId') || '0'),
          set: (value: number, remember: boolean) =>
            cookies.set('roleId', value.toString(), remember),
          remove: () => cookies.remove('roleId'),
        },
      }
    },
    token: (state) => {
      if (state.usingBCMS) {
        return useBCMSStore().token || ''
      }
      return state.userAuth?.token || ''
    },
    roleId: (state) => {
      if (!state.userAuth?.roleId || !state.isLogin) return 0
      return state.userAuth.roleId
    },
    role(): WebRole | null {
      if (!this.isLogin) {
        return null
      }
      const roleIdToRole: { [key: number]: WebRole } = {
        1: 'user',
      }
      return roleIdToRole[this.roleId]
    },
    apiRole(): ApiRole {
      const role = this.role
      if (!role) return 'beforeLogin'
      const map = {
        user: 'user',
      }
      return map[role as keyof typeof map] as ApiRole
    },

    isInBCMSRoute(): {
      router: Router
      isIn: boolean
    } {
      return {
        router,
        isIn: router.currentRoute.value.path.includes('bcms'),
      }
    },
  },
})
