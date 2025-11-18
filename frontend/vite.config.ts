import { fileURLToPath, URL } from 'node:url'
import { defineConfig, type ConfigEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'
import AutoImport from 'unplugin-auto-import/vite'

// Vite 配置
export default defineConfig(({ mode }: ConfigEnv) => {
  return {
    base: './',

    plugins: [
      vue(),
      WindiCSS(),
      AutoImport({
        imports: ['vue', 'vue-router'],
        dts: './src/auto-imports.d.ts',
        eslintrc: { enabled: true },
      }),
    ],

    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
      extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue', '.css'],
    },

    server: {
      watch: {
        usePolling: true,
      },
      // 這是設定 port 為 8080 的地方
      port: 8080,
    },

    build: {
      assetsDir: 'static',
      commonjsOptions: {
        include: [/node_modules/],
      },
      rollupOptions: {
        output: {
          chunkFileNames: 'js/[name]-[hash].js',
          entryFileNames: 'js/[name]-[hash].js',
          assetFileNames: (assetInfo) => {
            if (assetInfo.name?.endsWith('.css')) {
              return 'css/[name]-[hash].css'
            }
            return 'media/[name]-[hash][extname]'
          },
        },
      },
    },
  }
})
