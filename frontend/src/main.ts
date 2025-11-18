import { createApp } from 'vue'
import App from './App.vue'

// === 導入 Windi CSS (用於樣式設計) ===
// 這是 Windi CSS 透過 Vite 插件自動生成的樣式入口
import 'virtual:windi.css'

// === 導入第三方庫的全局 CSS ===
// 這是 Lottie 動畫庫的樣式，Rollup 會將其正確處理。
import 'vue3-lottie/dist/style.css'

// === 導入路由和狀態管理 ===
import router from './router'
import { createPinia } from 'pinia'

// 建立 Pinia 實例
const pinia = createPinia()

const app = createApp(App)

// 註冊 Pinia 和 Vue Router
app.use(pinia)
app.use(router)

// 掛載應用程式
app.mount('#app')
