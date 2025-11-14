import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'

// https://vitejs.dev/config/
export default defineConfig({
  // 確保 Vite 輸出時使用相對路徑，避免 Nginx 服務時出現 404
  base: './',
  plugins: [vue(), WindiCSS()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    // 解決 Docker Volume Mounts (Windows/Linux) 下 HMR 失敗的核心設置
    watch: {
      usePolling: true,
    },
  },
})
