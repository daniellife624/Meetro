import axios from 'axios'
// 引入 Store (注意：在攔截器中使用 Store 需小心循環引用，但在 Vue 3 + Pinia 通常沒問題)
import { useRoleStore } from '@/stores/modules/useRole'

const service = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 20000,
})

// 【新增】Request Interceptor：自動帶上 Token
service.interceptors.request.use(
  (config) => {
    const roleStore = useRoleStore()
    const token = roleStore.token // 從 Pinia 取得 Token

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response Interceptor (保持原樣，或是加上 401 自動登出)
service.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)

    // 建議加上：如果 Token 過期 (401)，自動登出並導向登入頁
    if (error.response && error.response.status === 401) {
      const roleStore = useRoleStore()
      roleStore.logout()
      window.location.href = '/web/login' // 強制導向
    }

    return Promise.reject(error)
  },
)

export default service
