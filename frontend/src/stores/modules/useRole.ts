import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 定義身份類型，確保類別安全
export type RoleType = 'guest' | 'user' | 'admin'

export const useRoleStore = defineStore('role', () => {
  // --- State ---
  // 預設身份為訪客 ('guest')
  // 如果想做持久化(重新整理後保持登入)，可以先從 localStorage 讀取
  const role = ref<RoleType>((localStorage.getItem('meetro_role') as RoleType) || 'guest')

  // --- Getters (Computed) ---
  // 取得目前身份
  const currentRole = computed(() => role.value)

  // 判斷式輔助函式 (方便在 template 中使用 v-if)
  const isGuest = computed(() => role.value === 'guest')
  const isUser = computed(() => role.value === 'user')
  const isAdmin = computed(() => role.value === 'admin')

  // --- Actions ---
  /**
   * 設定身份通用函式
   * @param newRole 新的身份
   */
  function setRole(newRole: RoleType) {
    role.value = newRole
    // 同步寫入 localStorage (模擬持久化)
    localStorage.setItem('meetro_role', newRole)
  }

  /**
   * 模擬使用者登入
   */
  function loginAsUser() {
    setRole('user')
  }

  /**
   * 模擬管理員登入 (後台)
   */
  function loginAsAdmin() {
    setRole('admin')
  }

  /**
   * 登出 (回到訪客狀態)
   */
  function logout() {
    setRole('guest')
    // 清除相關 Token (如果有)
    // localStorage.removeItem('token')
  }

  return {
    // State
    role,
    // Getters
    currentRole,
    isGuest,
    isUser,
    isAdmin,
    // Actions
    setRole,
    loginAsUser,
    loginAsAdmin,
    logout,
  }
})
