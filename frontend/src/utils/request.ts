import axios from 'axios'
// import { useRoleStore } from '@/stores/modules/useRole'

const service = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 20000,
})

// const getRoleStore = () => useRoleStore()

service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('meetro_token')

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

    // if (error.response && error.response.status === 401) {
    //   const roleStore = getRoleStore()
    //   roleStore.logout()
    //   window.location.href = '/web/login' // 強制導向
    // }

    return Promise.reject(error)
  },
)

export default service
