import useStorage from '@/composables/useStorage'
import { defineStore } from 'pinia'
// import { $bcmsApi } from '@/api/bcms'
// import { $notify } from '@/composables/useNotifications'
// import { BCMS } from '@/api/types/bcms'
import { useStore } from '..'

interface State {
  isLogin: boolean
  isInit: boolean
  token: string | null
}
const useBCMSStore = defineStore('bcms-main', {
  state: (): State => ({
    isLogin: false,
    isInit: false,
    token: null,
  }),
  actions: {
    auth() {
      this.isInit = true
      useStore().usingBCMS = true
      const token = useStorage('sessionStorage').get('token')
      if (token) this.updateAuth(token)
      return this.isLogin
      // this.updateRoute();
    },
    updateAuth(token: string | null) {
      const storage = useStorage('sessionStorage')
      if (token) {
        this.isLogin = true
        this.token = token
        storage.set('token', token)
      } else {
        this.isLogin = false
        this.token = null
        storage.clear('token')
      }
    },
    /**
     * 更新後台路由 暫棄
     */
    // updateRoute() {
    //   router.removeRoute("bcms");
    //   // 移除404
    //   router.removeRoute(notFoundRouteName);

    //   delete BCMSRoute.beforeEnter;
    //   router.addRoute(BCMSRoute);
    //   router.addRoute(notFoundRoute);
    // },

    async login(data: BCMS.LoginRequestData) {
      const { code, data: res } = await $bcmsApi.login(data)
      if (code === 200) {
        this.updateAuth(res.identifier)
        $notify.success('登入成功')
      }
      return code === 200
    },

    logout() {
      this.updateAuth(null)
    },
  },
})

export default useBCMSStore
