import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '@/utils/request'

export type RoleType = 'guest' | 'user' | 'admin'

export const useRoleStore = defineStore('role', () => {
  const role = ref<RoleType>((localStorage.getItem('meetro_role') as RoleType) || 'guest')
  const token = ref<string>(localStorage.getItem('meetro_token') || '')
  const isReady = ref(false)

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
    isReady.value = true
  }

  function setRole(newRole: RoleType) {
    role.value = newRole
    localStorage.setItem('meetro_role', newRole)
    isReady.value = true
  }

  // 新增 Action: 在刷新時，利用 Token 重新從後端獲取角色
  async function fetchUserRole() {
    console.log(
      '[RoleStore] Start fetching user role. Token exists:',
      !!token.value,
      'IsReady:',
      isReady.value,
    )
    if (token.value && !isReady.value) {
      try {
        // 呼叫後端 API 獲取當前使用者資訊
        const res: any = await request.get('/auth/me')
        role.value = (res.role as RoleType) || 'user'
      } catch (error) {
        console.error('Token 無效，清除登入狀態:', error)
        logout()
      } finally {
        isReady.value = true
      }
    } else if (!token.value) {
      isReady.value = true
    }
  }

  // 登出
  function logout() {
    role.value = 'guest'
    token.value = ''
    isReady.value = false
    localStorage.removeItem('meetro_role')
    localStorage.removeItem('meetro_token')
  }

  function loginAsUser() {
    setRole('user')
  }
  function loginAsAdmin() {
    setRole('admin')
  }

  return {
    role,
    token,
    isReady,
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
    fetchUserRole,
  }
})
