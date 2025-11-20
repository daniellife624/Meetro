<template>
  <header
    class="w-full h-16 sm:h-20 bg-[#008659] text-white px-4 md:px-8 flex items-center justify-between shadow-md font-sans z-50 relative"
  >
    <div class="flex items-center cursor-pointer" @click="goHome">
      <div class="w-8 h-8 sm:w-10 sm:h-10 bg-white rounded-sm mr-3 flex-shrink-0"></div>

      <h1 class="text-lg sm:text-xl font-bold tracking-wide truncate">
        <span v-if="currentRole === 'admin'">Meetro: 相遇地圖 ｜ 後臺管理端</span>
        <span v-else>Meetro: 相遇地圖</span>
      </h1>
    </div>

    <div class="flex items-center gap-4 sm:gap-6 md:gap-8 text-sm sm:text-base font-medium">
      <template v-if="currentRole === 'guest'">
        <button
          @click="goTeam"
          class="flex items-center gap-2 hover:text-green-100 transition-colors"
        >
          <SvgItem name="heart-hand" size="5" />
          <span class="hidden sm:inline">開發團隊</span>
        </button>
        <button
          @click="goLogin"
          class="flex items-center gap-2 hover:text-green-100 transition-colors"
        >
          <SvgItem name="login" size="5" />
          <span>登入</span>
        </button>
      </template>

      <template v-else-if="currentRole === 'user'">
        <button
          @click="goHistory"
          class="flex items-center gap-2 hover:text-green-100 transition-colors"
        >
          <SvgItem name="history" size="5" />
          <span class="hidden sm:inline">邀約歷史</span>
        </button>
        <button
          @click="goTeam"
          class="flex items-center gap-2 hover:text-green-100 transition-colors"
        >
          <SvgItem name="heart-hand" size="5" />
          <span class="hidden sm:inline">開發團隊</span>
        </button>
        <button
          @click="goProfile"
          class="flex items-center gap-2 hover:text-green-100 transition-colors"
        >
          <SvgItem name="user" size="5" />
          <span class="hidden sm:inline">我的帳戶</span>
        </button>
        <button
          @click="handleLogout"
          class="flex items-center gap-2 hover:text-green-100 transition-colors"
        >
          <SvgItem name="logout" size="5" />
          <span>登出</span>
        </button>
      </template>

      <template v-else-if="currentRole === 'admin'">
        <button
          @click="handleLogout"
          class="flex items-center gap-2 hover:text-green-100 transition-colors"
        >
          <SvgItem name="logout" size="5" />
          <span>登出</span>
        </button>
      </template>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRoleStore } from '@/stores/modules/useRole'
// 引入統一管理的 SVG 組件
import SvgItem from '@/components/icons/SvgItem.vue'

const router = useRouter()
const roleStore = useRoleStore()

// 使用 store 的 computed 屬性
const currentRole = computed(() => roleStore.currentRole)

// --- 導航邏輯 ---
const goHome = () => router.push('/')
const goTeam = () => router.push('/web/about')

const goLogin = () => {
  // 模擬登入流程：切換 Store 狀態並導航
  roleStore.loginAsUser()
  // 實際專案這裡應該導航到登入頁，例如 router.push('/login')
}

const goHistory = () => router.push('/web/history')
const goProfile = () => router.push('/web/profile')

const handleLogout = () => {
  if (confirm('確定要登出嗎？')) {
    roleStore.logout()
    router.push('/')
  }
}
</script>
