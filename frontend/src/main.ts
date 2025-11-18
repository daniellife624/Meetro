// src/main.ts - 應用程式進入點邏輯

import { createApp } from 'vue'
import App from './App.vue' // 導入根組件

// 導入 Pinia (狀態管理)
import { createPinia } from 'pinia'

// 🌟 關鍵修正：從新的位置 (src/router/index.ts) 導入 router 實例 🌟
import router from './router/index'

// 導入其他必要的樣式和庫
import 'virtual:windi.css' // 假設您有使用 Windi CSS

// 初始化應用程式
const app = createApp(App)

// 1. 掛載 Pinia (Pinia 必須先於 Router 掛載)
const pinia = createPinia()
app.use(pinia)

// 2. 掛載 Vue Router 實例
app.use(router)

// 3. 掛載到 HTML 根元素
app.mount('#app')
