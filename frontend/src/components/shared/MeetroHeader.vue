<template>
  <header
    class="header flex items-center w-full h-16 sm:h-20 2xl:h-24 bg-white px-2 md:px-4 xl:px-8 2xl:px-10 border-b border-gray-300"
  >
    <!-- 漢堡菜單圖標 (行動裝置) -->
    <div
      class="hamburger-icon xl:hidden flex items-center justify-center w-12 h-12 rounded-full cursor-pointer transition transform hover:bg-gray-200 duration-500"
      @click="isMenuShow = !isMenuShow"
    >
      <HamburgerIcon />
    </div>

    <!-- Meetro Logo / Home Link -->
    <router-link
      :to="{ name: 'home' }"
      class="flex items-center space-x-2 text-[#286047] text-xl font-bold h-full w-20 sm:w-24 lg:w-28 xl:w-32 2xl:w-36"
    >
      <div class="flex items-center h-full">
        <div
          class="w-6 h-6 sm:w-8 sm:h-8 bg-[#286047] rounded-full flex items-center justify-center text-white text-base font-extrabold mr-1"
        >
          M
        </div>
        <span class="text-sm sm:text-lg font-extrabold hidden lg:inline">Meetro</span>
      </div>
    </router-link>

    <!-- 功能列 (桌面版) -->
    <div class="hidden xl:flex items-center ml-auto">
      <template v-for="(item, index) in navList" :key="index">
        <!-- 假設 NavButton 能夠處理 item 數據並渲染 RouterLink 或下拉菜單 -->
        <NavButton :item="item" />
        <template v-if="index !== navList.length - 1">
          <!-- Divider 是分隔線組件 -->
          <Divider style="height: 36px" vertical />
        </template>
      </template>
    </div>

    <!-- 用戶按鈕 (登入狀態下顯示) -->
    <!-- UserBtn 應該包含登出和個人檔案下拉菜單的邏輯 -->
    <UserBtn v-if="isLogin" class="ml-auto xl:ml-[unset]" />

    <!-- 手機板導航抽屜 -->
    <Transition name="slide">
      <DrawerNavigation
        v-click-outside="{
          handler: () => (isMenuShow = false),
          safelist: ['.header .hamburger-icon'],
        }"
        v-show="isMenuShow"
        v-model="isMenuShow"
      />
    </Transition>
  </header>
</template>

<script setup>
import DrawerNavigation from '@/components/shared/DrawerNavigation.vue'
import NavButton from '@/components/buttons/NavButton.vue'

import { ref, computed } from 'vue'
import { useStore } from '@/stores'
import UserBtn from './UserBtn.vue'
import Divider from './Divider.vue'
import { useRole } from '@/composables/usePiniaOrRouter'

/*Icons*/
import HamburgerIcon from '@/components/icons/HamburgerIcon.vue'

const isMenuShow = ref(false)

// 假設 useStore 提供了 navGrouped 列表
const store = useStore()
const navList = computed(() => store.navGrouped)

// 假設 useRole 提供了 isLogin 狀態
const { isLogin } = useRole()
</script>

<style scoped>
/* 手機版菜單滑入/滑出動畫 */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
