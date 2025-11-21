<template>
  <div class="min-h-screen w-full flex bg-white font-sans overflow-hidden">
    <AuthSidePanel />

    <div class="w-full lg:w-1/2 flex items-center justify-center p-4 pb-32 bg-white min-h-screen">
      <div
        class="w-full max-w-md p-8 border-[3px] border-[#008659] rounded-[30px] shadow-xl bg-white relative flex flex-col max-h-[90vh] overflow-y-auto scrollbar-hide"
      >
        <h1
          class="text-3xl font-bold text-[#008659] text-center mb-6 tracking-widest flex-shrink-0"
        >
          會員登入
        </h1>

        <form @submit.prevent="handleLogin" class="space-y-5 flex-grow">
          <div class="space-y-1">
            <label class="flex items-center text-base font-bold text-gray-800">
              <SvgItem name="user-solid" size="5" class="text-[#008659] mr-2" filled />
              帳號 (Gmail)
            </label>
            <input
              v-model="form.username"
              type="email"
              placeholder="example@gmail.com"
              class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-[#008659] focus:ring-2 focus:ring-green-100 outline-none transition text-gray-600"
              required
            />
          </div>

          <div class="space-y-1">
            <label class="flex items-center text-base font-bold text-gray-800">
              <SvgItem name="lock" size="5" class="text-[#008659] mr-2" />
              密碼
            </label>
            <input
              v-model="form.password"
              type="password"
              placeholder="輸入密碼"
              class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-[#008659] focus:ring-2 focus:ring-green-100 outline-none transition text-gray-600"
              required
            />
          </div>

          <div
            class="flex justify-center items-center text-sm sm:text-base font-bold text-[#008659] space-x-2 pt-2"
          >
            <router-link :to="{ name: 'WebRegister' }" class="hover:underline hover:text-[#006d48]">
              尚未註冊（馬上註冊體驗）
            </router-link>
            <span class="text-gray-400">|</span>
            <button type="button" class="hover:underline hover:text-[#006d48]">忘記密碼</button>
          </div>

          <button
            type="submit"
            class="w-full py-3 bg-[#008659] text-white text-xl font-bold rounded-full shadow-lg hover:bg-[#006d48] hover:shadow-xl transform active:scale-95 transition duration-200 mt-4"
          >
            登入
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useRoleStore } from '@/stores/modules/useRole'
import { useLoadingStore } from '@/stores/modules/loading'
import SvgItem from '@/components/icons/SvgItem.vue'
import AuthSidePanel from '@/components/shared/AuthSidePanel.vue'

const router = useRouter()
const route = useRoute()
const roleStore = useRoleStore()
const loadingStore = useLoadingStore()

const form = reactive({
  username: '',
  password: '',
})

const handleLogin = async () => {
  loadingStore.setLoading(true, '登入中...')
  try {
    await new Promise((resolve) => setTimeout(resolve, 1000))
    roleStore.loginAsUser()
    const redirectPath = route.query.redirect as string
    router.push(redirectPath || '/')
  } catch (error) {
    console.error(error)
    alert('登入失敗')
  } finally {
    loadingStore.setLoading(false)
  }
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
