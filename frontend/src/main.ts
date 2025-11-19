import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'virtual:windi.css'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/modules/auth'
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
async function bootstrap() {
  try {
    // 獲取 Auth Store 實例 (確保 pinia 已經 app.use(pinia))
    const authStore = useAuthStore()

    // 🌟 關鍵：等待 Auth Store 執行動態路由新增和首次導航
    // initApp 必須在 app.mount 之前完成，確保所有路由都已準備就緒
    await authStore.initApp()

    // 只有在路由和應用程式狀態完全初始化後才掛載 Vue 應用程式
    app.mount('#app')
    console.log('應用程式成功掛載！')
  } catch (error) {
    console.error('應用程式啟動失敗:', error)
    // 可以在此處顯示一個友善的錯誤訊息給使用者
  }
}

// 執行應用程式啟動流程
bootstrap()
