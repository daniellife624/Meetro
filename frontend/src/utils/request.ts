import axios from 'axios'

const service = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 20000,
})

service.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  },
)

export default service
