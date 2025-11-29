// src/composables/useRole.ts

import { computed, ref } from 'vue'
import type { Ref } from 'vue'

type UserRole = 'guest' | 'authenticated' | 'admin' | 'bcms_user'

/**
 * 模擬一個用戶角色管理的 Composable。
 * 在實際應用中，它會與你的身份驗證/Store 系統整合。
 */
export function useRole() {
  const currentRole: Ref<UserRole> = ref('authenticated')
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
    return currentRole.value === 'bcms_user' || currentRole.value === 'admin'
  })

  /**
   * 設定新的角色 (實際應用中可能透過登入/登出流程呼叫)
   */
  function setRole(newRole: UserRole) {
    currentRole.value = newRole
  }

  return {
    currentRole,
    userId,
    isAdmin,
    isAuthenticated,
    isBcmsUser,
    setRole,
  }
}
