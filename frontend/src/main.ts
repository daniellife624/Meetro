import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'virtual:windi.css'
import App from './App.vue'
import router from './router'
// import { useAuthStore } from './stores/modules/auth'
import './assets/global.css'

// import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

/**
 * @description 應用程式啟動函式。
 * 負責初始化所有服務，例如 Pinia Store 的狀態和動態路由。
 */

app.mount('#app')
console.log('應用程式成功掛載！')
