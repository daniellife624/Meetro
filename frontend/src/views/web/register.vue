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
          註冊會員
        </h1>

        <form @submit.prevent="handleRegister" class="space-y-5 flex-grow">
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

          <div class="space-y-1">
            <label class="flex items-center text-base font-bold text-gray-800">
              <SvgItem name="check" size="5" class="text-[#008659] mr-2" />
              確認密碼
            </label>
            <input
              v-model="form.confirmPassword"
              type="password"
              placeholder="請再次輸入密碼"
              class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-[#008659] focus:ring-2 focus:ring-green-100 outline-none transition text-gray-600"
              required
            />
          </div>

          <div class="space-y-1">
            <label class="flex items-center text-base font-bold text-gray-800">
              <SvgItem name="smile" size="5" class="text-[#008659] mr-2" />
              姓名
            </label>
            <input
              v-model="form.name"
              type="text"
              placeholder="請輸入您的姓名或暱稱"
              class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-[#008659] focus:ring-2 focus:ring-green-100 outline-none transition text-gray-600"
              required
            />
          </div>

          <div class="space-y-1">
            <label class="flex items-center text-base font-bold text-gray-800">
              <SvgItem name="calendar" size="5" class="text-[#008659] mr-2" />
              生日
            </label>
            <input
              v-model="form.birthday"
              type="date"
              class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-[#008659] focus:ring-2 focus:ring-green-100 outline-none transition text-gray-600 bg-white"
              required
            />
          </div>

          <div class="space-y-1">
            <label class="flex items-center text-base font-bold text-gray-800">
              <SvgItem name="gender" size="5" class="text-[#008659] mr-2" />
              性別
            </label>
            <div class="relative">
              <select
                v-model="form.gender"
                class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-[#008659] focus:ring-2 focus:ring-green-100 outline-none transition text-gray-600 appearance-none bg-white"
                required
              >
                <option value="" disabled selected>請選擇性別</option>
                <option value="male">男性</option>
                <option value="female">女性</option>
                <option value="other">其他</option>
              </select>
              <div
                class="absolute inset-y-0 right-0 flex items-center px-4 pointer-events-none text-[#008659]"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  ></path>
                </svg>
              </div>
            </div>
          </div>

          <div
            class="flex justify-center items-center text-sm sm:text-base font-bold text-[#008659] space-x-2 pt-2"
          >
            <router-link :to="{ name: 'WebLogin' }" class="hover:underline hover:text-[#006d48]">
              已有帳號？馬上登入
            </router-link>
          </div>

          <button
            type="submit"
            class="w-full py-3 bg-[#008659] text-white text-xl font-bold rounded-full shadow-lg hover:bg-[#006d48] hover:shadow-xl transform active:scale-95 transition duration-200 mt-4"
          >
            註冊
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useLoadingStore } from '@/stores/modules/loading'
import SvgItem from '@/components/icons/SvgItem.vue'
import AuthSidePanel from '@/components/shared/AuthSidePanel.vue'

const router = useRouter()
const loadingStore = useLoadingStore()

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  birthday: '',
  gender: '',
})

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    alert('兩次密碼輸入不一致！')
    return
  }

  loadingStore.setLoading(true, '註冊中...')

  try {
    await new Promise((resolve) => setTimeout(resolve, 1000))

    console.log('註冊 Payload:', form)
    alert('註冊成功！請使用新帳號登入。')

    router.push({ name: 'WebLogin' })
  } catch (error) {
    console.error(error)
    alert('註冊失敗')
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
