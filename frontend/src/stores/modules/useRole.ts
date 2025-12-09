import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type RoleType = 'guest' | 'user' | 'admin'

export const useRoleStore = defineStore('role', () => {
  const role = ref<RoleType>((localStorage.getItem('meetro_role') as RoleType) || 'guest')
  const token = ref<string>(localStorage.getItem('meetro_token') || '')

  const currentRole = computed(() => role.value)
  const isGuest = computed(() => role.value === 'guest')
  const isUser = computed(() => role.value === 'user')
  const isAdmin = computed(() => role.value === 'admin')
  const isAuthenticated = computed(() => !!token.value)

  // 設定登入狀態 (同時存 role 和 token)
  function setLoginState(newRole: RoleType, newToken: string) {
    role.value = newRole
    token.value = newToken
    localStorage.setItem('meetro_role', newRole)
    localStorage.setItem('meetro_token', newToken)
  }

  // 純設定身分 (保留給舊代碼相容，或手動切換用)
  function setRole(newRole: RoleType) {
    role.value = newRole
    localStorage.setItem('meetro_role', newRole)
  }

  // 登出
  function logout() {
    role.value = 'guest'
    token.value = ''
    localStorage.removeItem('meetro_role')
    localStorage.removeItem('meetro_token')
  }

  // 模擬登入
  function loginAsUser() {
    setRole('user')
  }
  function loginAsAdmin() {
    setRole('admin')
  }

  return {
    role,
    token, // 匯出 token
    currentRole,
    isGuest,
    isUser,
    isAdmin,
    isAuthenticated,
    setRole,
    setLoginState,
    loginAsUser,
    loginAsAdmin,
    logout,
  }
})
