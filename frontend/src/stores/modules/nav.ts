import { defineStore } from 'pinia'
import { computed } from 'vue'
import type { NavItem } from '@/types/header/index.d.ts'

// 定義導航菜單的靜態資料
const BEFORE_LOGIN_NAV: NavItem[] = [
  { name: '開發團隊', icon: 'UserGroupIcon', type: 'router', routeName: 'Members' },
  { name: '登入', icon: 'ArrowRightOnRectangleIcon', type: 'router', routeName: 'Login' },
]

const AFTER_LOGIN_NAV: NavItem[] = [
  { name: '歷史紀錄', icon: 'ClockIcon', type: 'router', routeName: 'History' },
  { name: '開發團隊', icon: 'UserGroupIcon', type: 'router', routeName: 'Members' },
  { name: '個人資料', icon: 'UserCircleIcon', type: 'router', routeName: 'Profile' },
  { name: '登出', icon: 'ArrowLeftOnRectangleIcon', type: 'grouped' }, // type: 'grouped' 觸發登出邏輯
]

export const useNavStore = defineStore('nav', () => {
  // 為了讓 MeetroHeader.vue 中的 navList = computed(() => store.navGrouped) 邏輯跑通
  // 我們需要將登入後的菜單作為 'nav' (給手機版) 和 'navGrouped' (給桌面版) 輸出。

  // 這裡需要依賴 Auth Store 來決定輸出哪個列表
  function getNavList(isLoggedIn: boolean): NavItem[] {
    return isLoggedIn ? AFTER_LOGIN_NAV : BEFORE_LOGIN_NAV
  }

  // 由於 MeetroHeader.vue 引用了 store.navGrouped，我們在這裡定義一個簡單的 Getter
  const navGrouped = computed(() => AFTER_LOGIN_NAV)
  const nav = computed(() => AFTER_LOGIN_NAV)

  return { getNavList, navGrouped, nav }
})
