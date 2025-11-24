import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type RoleType = 'guest' | 'user' | 'admin'

export const useRoleStore = defineStore('role', () => {
  // --- 修正重點 1：State 初始化 ---
  // 不要只寫 ref('guest')
  // 要先嘗試從 localStorage 讀取，讀不到才用 'guest'
  const role = ref<RoleType>((localStorage.getItem('meetro_role') as RoleType) || 'guest')

  // --- Getters ---
  const currentRole = computed(() => role.value)
  const isGuest = computed(() => role.value === 'guest')
  const isUser = computed(() => role.value === 'user')
  const isAdmin = computed(() => role.value === 'admin')

  // --- 修正重點 2：Actions 寫入 ---
  // 每次改變身分時，都要同步寫入 localStorage
  function setRole(newRole: RoleType) {
    role.value = newRole
    localStorage.setItem('meetro_role', newRole)
  }

  function loginAsUser() {
    setRole('user')
  }

  function loginAsAdmin() {
    setRole('admin')
  }

  function logout() {
    setRole('guest')
    localStorage.removeItem('meetro_role') // 登出時清除
  }

  return {
    role,
    currentRole,
    isGuest,
    isUser,
    isAdmin,
    setRole,
    loginAsUser,
    loginAsAdmin,
    logout,
  }
})
