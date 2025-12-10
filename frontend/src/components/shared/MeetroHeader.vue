<template>
  <header class="w-full h-16 sm:h-20 bg-[#008659] shadow-md font-sans z-50 relative">
    <div class="w-full h-full px-4 md:px-8 flex items-center justify-between text-white">
      <div class="flex items-center cursor-pointer" @click="goHome">
        <div class="w-5 h-5 sm:w-6 sm:h-6 mr-3 flex-shrink-0">
          <SvgItem name="heart-hand" size="full" class="text-white rounded-sm" />
        </div>

        <h1 class="text-lg sm:text-xl font-bold tracking-wide truncate">
          <span v-if="currentRole === 'admin'">Meetro: 相遇地圖 ｜ 後臺管理端</span>
          <span v-else>Meetro: 相遇地圖</span>
        </h1>
      </div>

      <div
        class="hidden md:flex items-center gap-3 sm:gap-4 md:gap-6 font-bold text-sm lg:text-base"
      >
        <template v-if="currentRole === 'guest'">
          <!-- <button
            @click="goTeam"
            class="flex items-center gap-2 hover:text-green-100 transition-colors"
          >
            <SvgItem name="heart-hand" size="5" />
            <span class="hidden sm:inline">開發團隊</span>
          </button> -->
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
          <!-- <button
            @click="goTeam"
            class="flex items-center gap-2 hover:text-green-100 transition-colors"
          >
            <SvgItem name="heart-hand" size="5" />
            <span class="hidden sm:inline">開發團隊</span>
          </button> -->
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

      <div class="flex md:hidden">
        <button
          @click="isDrawerOpen = true"
          class="p-2 hover:bg-white/10 rounded-full transition-colors"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
      </div>
    </div>

    <DrawerNavigation
      v-model="isDrawerOpen"
      :current-role="currentRole"
      @go-home="goHome"
      @go-login="goLogin"
      @go-history="goHistory"
      @go-team="goTeam"
      @go-profile="goProfile"
      @logout="handleLogout"
    />
  </header>
</template>

<script setup lang="ts">
// Script 內容完全不用動
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRoleStore } from '@/stores/modules/useRole'
import SvgItem from '@/components/icons/SvgItem.vue'
import DrawerNavigation from '@/components/shared/DrawerNavigation.vue'

const router = useRouter()
const roleStore = useRoleStore()

const currentRole = computed(() => roleStore.currentRole)
const isDrawerOpen = ref(false)

const goHome = () => {
  isDrawerOpen.value = false
  router.push('/')
}
const goTeam = () => {
  isDrawerOpen.value = false
  router.push('/web/about')
}
const goLogin = () => {
  isDrawerOpen.value = false
  router.push({ name: 'WebLogin' })
}
const goHistory = () => {
  isDrawerOpen.value = false
  router.push('/web/history')
}
const goProfile = () => {
  isDrawerOpen.value = false
  router.push('/web/profile')
}

const handleLogout = () => {
  if (confirm('確定要登出嗎？')) {
    const wasAdmin = roleStore.isAdmin
    roleStore.logout()
    if (wasAdmin) {
      router.push({ name: 'BCMSLogin' })
    } else {
      router.push({ name: 'home' })
    }
    isDrawerOpen.value = false
  }
}
</script>
