<template>
  <div class="min-h-screen w-full flex flex-col bg-white font-sans overflow-hidden">
    <header class="w-full h-16 bg-[#008659] flex items-center px-6 shadow-md z-20">
      <div class="flex items-center gap-4">
        <div class="w-10 h-10 bg-white rounded-sm flex-shrink-0"></div>
        <h1 class="text-xl font-bold text-white tracking-wide flex items-center gap-3">
          <span>Meetro: 相遇地圖</span>
          <span class="text-white/50 text-2xl font-light">|</span>
          <span>後臺管理端</span>
        </h1>
      </div>
    </header>

    <main class="flex-grow flex items-center justify-center p-4 relative z-10">
      <div
        class="w-full max-w-lg p-10 bg-white border-[3px] border-gray-300 rounded-[30px] shadow-2xl flex flex-col"
      >
        <h2 class="text-3xl font-bold text-gray-600 text-center mb-10 tracking-widest">
          管理後臺入口
        </h2>

        <form @submit.prevent="handleLogin" class="space-y-8">
          <div class="space-y-2">
            <label class="flex items-center text-lg font-bold text-gray-800">
              <SvgItem name="user-solid" size="6" class="text-[#333] mr-2" filled />
              帳號
            </label>
            <input
              v-model="form.username"
              type="text"
              placeholder="輸入登入帳號"
              class="w-full px-4 py-3.5 rounded-xl border border-gray-300 focus:border-[#5e5e5e] focus:ring-2 focus:ring-gray-200 outline-none transition text-gray-600 text-lg"
              required
            />
          </div>

          <div class="space-y-2">
            <label class="flex items-center text-lg font-bold text-gray-800">
              <SvgItem name="lock" size="5" class="text-[#008659] mr-2" />
              密碼
            </label>
            <input
              v-model="form.password"
              type="password"
              placeholder="輸入登入密碼"
              class="w-full px-4 py-3.5 rounded-xl border border-gray-300 focus:border-[#5e5e5e] focus:ring-2 focus:ring-gray-200 outline-none transition text-gray-600 text-lg"
              required
            />
          </div>

          <button
            type="submit"
            class="w-1/2 mx-auto block py-3 bg-[#5e5e5e] text-white text-xl font-bold rounded-full shadow-lg hover:bg-[#4a4a4a] hover:shadow-xl transform active:scale-95 transition duration-200 mt-4"
          >
            登入
          </button>
        </form>
      </div>
    </main>

    <footer
      class="w-full bg-[#5e5e5e] text-white text-center py-4 text-sm font-light tracking-wider z-20"
    >
      &copy; 2025 MeetTro 相遇地圖 版權所有
    </footer>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useRoleStore } from '@/stores/modules/useRole'
import { useLoadingStore } from '@/stores/modules/loading'
import SvgItem from '@/components/icons/SvgItem.vue'

const router = useRouter()
const roleStore = useRoleStore()
const loadingStore = useLoadingStore()

const form = reactive({
  username: '',
  password: '',
})

const handleLogin = async () => {
  loadingStore.setLoading(true, '系統登入中...')

  try {
    await new Promise((resolve) => setTimeout(resolve, 800))

    // 測試帳號: admin
    if (form.username === 'admin') {
      console.log('後台登入成功')
      roleStore.loginAsAdmin()
      // 導航至後台儀表板
      router.push({ name: 'BCMSDashboard' })
    } else {
      alert('帳號或密碼錯誤 (測試帳號: admin)')
    }
  } catch (error) {
    console.error(error)
    alert('登入失敗')
  } finally {
    loadingStore.setLoading(false)
  }
}
</script>

<style scoped>
:deep(svg) {
  color: #333;
}
</style>
