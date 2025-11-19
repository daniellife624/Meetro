// src/composables/useRole.ts

import { computed, ref } from 'vue'
import type { Ref } from 'vue'

// 假設的角色類型，可根據你的應用程式實際情況調整
type UserRole = 'guest' | 'authenticated' | 'admin' | 'bcms_user'

/**
 * 模擬一個用戶角色管理的 Composable。
 * 在實際應用中，它會與你的身份驗證/Store 系統整合。
 */
export function useRole() {
  // 這裡使用 ref 模擬當前登入用戶的角色狀態
  // 初始值設為 'guest' 或從你的 Store/Auth 服務中獲取
  const currentRole: Ref<UserRole> = ref('authenticated')

  // 模擬用戶 ID (例如，用於 BCMS 頁面)
  const userId: Ref<string | null> = ref('user-12345')

  /**
   * 檢查用戶是否具有管理員角色
   */
  const isAdmin = computed(() => {
    return currentRole.value === 'admin'
  })

  /**
   * 檢查用戶是否已登入（非訪客）
   */
  const isAuthenticated = computed(() => {
    return currentRole.value !== 'guest'
  })

  /**
   * 檢查用戶是否可以存取後臺管理系統 (BCMS)
   */
  const isBcmsUser = computed(() => {
    // 假設 'admin' 角色也可以存取 BCMS
    return currentRole.value === 'bcms_user' || currentRole.value === 'admin'
  })

  /**
   * 設定新的角色 (實際應用中可能透過登入/登出流程呼叫)
   */
  function setRole(newRole: UserRole) {
    currentRole.value = newRole
  }

  // 為了防止編譯失敗，我們假設 MeetroHeader 需要這些導出
  return {
    currentRole,
    userId,
    isAdmin,
    isAuthenticated,
    isBcmsUser,
    setRole,
  }
}
