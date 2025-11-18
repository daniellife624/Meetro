import router from '@/router'
// import { $notify } from '@/composables/useNotifications'
import { notFoundRouteName } from '@/router/modules/404'
import { NavigationGuardWithThis, RouteRecordRaw } from 'vue-router'
// import { WebRole } from '@/types/web'
// import { useStore } from '@/store'
// import { useRole } from '@/composables/usePiniaOrRouter'

export const webRouteName = 'web-index'
/**
 * web root route
 */
export const getWebRoute = (children: RouteRecordRaw[]): RouteRecordRaw => ({
  path: '/',
  name: webRouteName,
  component: () => import('@/views/web.vue'),
  redirect: { name: 'home' },
  beforeEnter: (to, from) => {
    const store = useStore()
    if (!store.isInit) {
      const router = store.auth()
      if (to.name && router.hasRoute(to.name))
        return { name: to.name, params: to.params, query: to.query }
      else return { path: to.fullPath, params: to.params, query: to.query }
    }
  },
  children,
})

const ChatItem = () => import('@/components/web/shared/ChatItem.vue')
const BackToTop = () => import('@/components/web/shared/BackToTop.vue')

function getTitle(text: string) {
  return `${text} - Meetro`
}

export class RouteModel {
  _role: WebRole = null
  _all: boolean = false
  constructor(role: WebRole, all: boolean = false) {
    this._role = role
    this._all = all
  }

  // 首頁(登入前)
  home = () => {
    return {
      path: '',
      name: 'home',
      meta: {
        role: this._role,
        title: getTitle('首頁'),
      },
      components: {
        default: () => import('@/views/web/index.vue'),
        BackToTop,
      },
    }
  }
  //登入
  login = () => ({
    path: 'login',
    name: 'login',
    meta: {
      title: getTitle('登入'),
      mainClass: 'flex items-center',
    },
    components: {
      default: () => import('@/views/web/login.vue'),
    },
  })
  //註冊
  register = () => ({
    path: 'register',
    name: 'register',
    meta: {
      title: getTitle('註冊'),
    },
    components: {
      default: () => import('@/views/web/register.vue'),
      BackToTop,
    },
  })
  //忘記密碼
  forgetPassword = () => ({
    path: 'forgetPassword',
    name: 'forget-password',
    meta: {
      title: getTitle('忘記密碼'),
      mainClass: 'flex items-center',
    },
    components: {
      default: () => import('@/views/web/ForgetPassword.vue'),
    },
  })

  //   questions = () => {
  //     return {
  //       path: `questions`,
  //       name: `questions`,
  //       meta: {
  //         role: this._role,
  //       },
  //       components: {
  //         default: () => import(`@/views/web/questions.vue`),
  //         BackToTop,
  //       },
  //     }
  //   }

  // 通知中心(選擇方)
  //   notifications = () => {
  //     return {
  //       path: `notifications`,
  //       name: `notifications`,
  //       meta: {
  //         role: this._role,
  //       },
  //       components: {
  //         default: () => import(`@/views/web/notifications.vue`),
  //         ChatItem,
  //         BackToTop,
  //       },
  //     }
  //   }

  // 我的收藏商家(消費者端)
  //   favorites = () => {
  //     return {
  //       path: 'favorites',
  //       name: `favorites`,
  //       meta: {
  //         role: this._role,
  //       },
  //       components: {
  //         default: () => import('@/views/web/favorites.vue'),
  //         BackToTop,
  //         ChatItem,
  //       },
  //     }
  //   }

  // 個人資料頁(消費者端、店家端、組織端)
  profile = () => {
    return {
      path: 'profile',
      components: {
        default: () => import('@/views/web/profile.vue'),
        BackToTop,
        ChatItem,
      },
      children: [
        {
          path: '',
          name: `profile`,
          component: () => import('@/views/web/profile/index.vue'),
        },
        {
          path: 'update',
          name: `profile-update`,
          component: () => import('@/views/web/profile/update.vue'),
        },
      ],
    }
  }

  // 活動(消費者端、組織端)
  //   events = () => {
  //     const role = this._role
  //     const children: RouteRecordRaw[] = [
  //       {
  //         path: '',
  //         name: 'events',
  //         component: () => import('@/views/web/events/index.vue'),
  //       },
  //       {
  //         path: ':id(\\d+)',
  //         name: 'events-id',
  //         component: () => import('@/views/web/events/id.vue'),
  //       },
  //     ]
  //     const eventsAction = [
  //       {
  //         path: 'create',
  //         name: `events-create`,
  //         component: () => import('@/views/web/events/create.vue'),
  //       },
  //       {
  //         path: ':id(\\d+)/update',
  //         name: 'events-update',
  //         component: () => import('@/views/web/events/update.vue'),
  //       },
  //     ]
  //     if (role === 'organization' || this._all) children.push(...eventsAction)
  //     return {
  //       path: 'events',
  //       meta: { role },
  //       beforeEnter: merchantAuth,
  //       components: {
  //         default: () => import('@/views/web/events.vue'),
  //         BackToTop,
  //         ChatItem,
  //       },
  //       children,
  //       redirect: { name: 'events' },
  //     }
  //   }

  //   upgrade = () => {
  //     const role = this._role
  //     return {
  //       path: `upgrade`,
  //       meta: { role },
  //       components: {
  //         default: () => import('@/views/web/upgrade.vue'),
  //         BackToTop,
  //         ChatItem,
  //       },
  //       children: [
  //         {
  //           path: '',
  //           name: `upgrade`,
  //           component: () => import('@/views/web/upgrade/index.vue'),
  //         },
  //         {
  //           beforeEnter: merchantAuth,
  //           path: 'details',
  //           component: () => import('@/views/web/upgrade/details.vue'),
  //           children: [
  //             {
  //               name: `upgrade-details`,
  //               path: '',
  //               component: () => import('@/views/web/upgrade/details/index.vue'),
  //             },
  //             {
  //               name: `upgrade-details-id`,
  //               path: ':id(\\d+)',
  //               component: () => import('@/views/web/upgrade/details/id.vue'),
  //             },
  //           ],
  //         },
  //         {
  //           path: 'points',
  //           name: `upgrade-points`,
  //           beforeEnter: merchantAuth,
  //           component: () => import('@/views/web/upgrade/points.vue'),
  //         },
  //         {
  //           path: 'ads',
  //           name: `upgrade-ads`,
  //           beforeEnter: merchantAuth,
  //           component: () => import('@/views/web/upgrade/ads.vue'),
  //         },
  //       ],
  //     }
  //   }
}
