import axios from 'axios'
import { useRoleStore } from '@/stores/modules/useRole'

const service = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 20000,
})

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

// Response Interceptor
service.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)

    if (error.response && error.response.status === 401) {
      const roleStore = useRoleStore()
      roleStore.logout()
      window.location.href = '/web/login' // 強制導向
    }

    return Promise.reject(error)
  },
)

export default service
