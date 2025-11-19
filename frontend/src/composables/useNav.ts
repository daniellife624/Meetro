// import { useNotificationStore } from '@/store/modules/notifications'
import { NavItem } from '../types/header/header'
import { WebRole } from '@/types/web'
import { computed, defineAsyncComponent } from 'vue'
import { useRole } from './usePiniaOrRouter'

// Before Login
const MemberIcon = defineAsyncComponent(() => import('@/components/icons/MemberIcon.vue'))
const LoginIcon = defineAsyncComponent(() => import('@/components/icons/LoginIcon.vue'))
// const BellIcon = defineAsyncComponent(() => import('@/components/icons/BellIcon.vue'))

// User
// const AssignmentIcon = defineAsyncComponent(() => import('@/components/icons/AssignmentIcon.vue'))
// const HeartIcon = defineAsyncComponent(() => import('@/components/icons/HeartIcon.vue'))
const HistoryIcon = defineAsyncComponent(() => import('@/components/icons/HistoryIcon.vue'))
// MemberIcon
const ProfileIcon = defineAsyncComponent(() => import('@/components/icons/ProfileIcon.vue'))
// const LogoutIcon = defineAsyncComponent(() => import('@/components/icons/LogoutIcon.vue'))
const ChevronDownIcon = defineAsyncComponent(() => import('@/components/icons/ChevronDownIcon.vue'))

const nav = computed(() => {
  const { role } = useRole()
  //   const notificationStore = useNotificationStore()
  const allNavList = {
    // 登入前
    login: {
      name: '登入',
      icon: 'LoginIcon',
      routeName: 'login',
      type: 'router',
    },
    members: {
      name: '開發團隊',
      icon: 'MemberIcon',
      routeName: 'members',
      type: 'router',
    },
    // 登入後
    // notifications: {
    //   name: '通知中心',
    //   icon: 'BellIcon',
    //   routeName: 'notifications',
    //   type: 'router',
    //   count: notificationStore.notificationUnreadCount,
    // },

    // User
    history: {
      name: '邀約歷史',
      icon: 'HistoryIcon',
      routeName: 'history',
      type: 'router',
    },
    // favorites: {
    //   name: '收藏店家',
    //   icon: 'HeartIcon',
    //   routeName: 'favorites',
    //   type: 'router',
    // },
    profile: {
      name: '我的帳戶',
      icon: 'ProfileIcon',
      routeName: 'profile',
      type: 'router',
    },
    // logout: {
    //   name: '登出',
    //   icon: 'LogoutIcon',
    //   routeName: 'logout',
    //   type: 'router',
    // },
  }
  return allNavList as { [key in keyof typeof allNavList]: NavItem }
})

function getGroupedNavItem(name: string, children: NavItem[]) {
  return {
    name,
    children,
    icon: 'ChevronDownIcon',
    type: 'grouped',
  } as NavItem
}

export const getNavList = (role: WebRole, grouped: boolean = false): NavItem[] => {
  //未登入
  if (!role) return [nav.value.login, nav.value.members]
  const userNavMap = [
    nav.value.history,
    nav.value.members,
    nav.value.profile,
    // nav.value.notifications,
  ]

  const navMap: { [key in Exclude<WebRole, null>]: NavItem[] } = {
    user: userNavMap,
  }
  return navMap[role]
}

export const navIcons = {
  // Before Login
  LoginIcon,
  MemberIcon,
  // BellIcon,

  // User
  // HeartIcon,
  HistoryIcon,
  ProfileIcon,
  ChevronDownIcon,
}
