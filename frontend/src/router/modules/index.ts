import { RouteRecordRaw } from 'vue-router'

// 這是路由巢狀結構的基礎路徑名稱，用於動態添加路由
export const webRouteName = 'web'

/**
 * @description 取得 RouteRecordRaw，用於在 Store 中動態新增路由模組。
 * @param children 傳入特定角色的子路由列表
 * @returns 完整的 web 父級路由物件
 */
export const getWebRoute = (children: RouteRecordRaw[]): RouteRecordRaw => ({
  path: '/web',
  name: webRouteName,
  component: () => import('@/views/web/index.vue'),
  children,
})

/**
 * @description 建立標準路由物件的 Helper Class，確保命名和路徑一致性。
 * @param role 角色名稱 ('user', 'beforeLogin', 'bcms' 等)，用於 meta.roles
 */
export class RouteModel {
  role: string | null

  constructor(role: string | null) {
    this.role = role
  }

  // 靜態方法，用於統一的 meta 屬性
  private getMeta(title: string, requiresAuth: boolean = false) {
    return {
      title,
      requiresAuth,
      roles: this.role ? [this.role] : [],
    }
  }

  // 首頁/根目錄路由
  home(): RouteRecordRaw {
    return {
      path: '', // 繼承父級 '/web'
      name: 'home', // 應用程式入口預設名稱
      meta: this.getMeta('首頁', !!this.role),
      component: () => import('@/views/web/index.vue'),
    }
  }

  // 登入頁面 (僅限 BeforeLogin 使用)
  login(): RouteRecordRaw {
    return {
      path: 'login',
      name: 'Login',
      meta: this.getMeta('登入'),
      component: () => import('@/views/web/login.vue'),
    }
  }

  // 註冊頁面 (僅限 BeforeLogin 使用)
  register(): RouteRecordRaw {
    return {
      path: 'register',
      name: 'Register',
      meta: this.getMeta('註冊'),
      component: () => import('@/views/web/register.vue'),
    }
  }

  // 忘記密碼頁面 (僅限 BeforeLogin 使用)
  forgetPassword(): RouteRecordRaw {
    return {
      path: 'forget-password',
      name: 'ForgetPassword',
      meta: this.getMeta('忘記密碼'),
      component: () => import('@/views/web/ForgetPassword.vue'),
    }
  }

  // 個人資料頁面 (僅限 User 使用)
  profile(): RouteRecordRaw {
    return {
      path: 'profile',
      name: 'UserProfile',
      meta: this.getMeta('個人資料', true),
      component: () => import('@/views/web/profile.vue'),
    }
  }

  // 歷史記錄頁面 (僅限 User 使用)
  history(): RouteRecordRaw {
    return {
      path: 'history',
      name: 'UserHistory',
      meta: this.getMeta('歷史記錄', true),
      component: () => import('@/views/web/history.vue'),
    }
  }

  // 會員列表/社群頁面 (Both Roles 使用)
  members(): RouteRecordRaw {
    return {
      path: 'members',
      name: 'Members',
      // 未登入角色可見 (requiresAuth: false)，但 User 角色也能透過這個路由訪問
      meta: this.getMeta('會員列表', false),
      component: () => import('@/views/web/members.vue'),
    }
  }

  // 登出路由 (僅限 User 使用，通常觸發 Pinia action)
  // 這裡我們指向一個空的組件，並在 meta 中標記為登出動作
  logout(): RouteRecordRaw {
    return {
      path: 'logout',
      name: 'Logout',
      meta: this.getMeta('登出', true),
      // 通常登出不需要專門的組件，但這裡可以指向一個處理登出邏輯的頁面或空頁面
      component: () => import('@/views/web/LogoutPlaceholder.vue'),
    }
  }
}
