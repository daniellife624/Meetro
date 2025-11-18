import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv, type ConfigEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'

// 引入新的插件
import AutoImport from 'unplugin-auto-import/vite'
import viteCompression from 'vite-plugin-compression'

// 導出配置
export default defineConfig(({ mode }: ConfigEnv) => {
  const env = loadEnv(mode, process.cwd(), '')
  const IS_PROD = mode === 'production'
  const productionGzipExtensions = /\.(js|css|json|txt|html|ico|svg)$/i

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
      IS_PROD &&
        viteCompression({
          ext: '.gz',
          test: productionGzipExtensions,
          threshold: 10240,
          deleteOriginFile: false,
        }),
    ].filter(Boolean),

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
    },

    build: {
      assetsDir: 'static',

      commonjsOptions: {
        include: [/node_modules/],
      },

      rollupOptions: {
        // *** 修正：重新加入 external 設置，告訴 Rollup 忽略這個 Lottie CSS 檔案 ***
        external: ['vue3-lottie/dist/style.css'],

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
