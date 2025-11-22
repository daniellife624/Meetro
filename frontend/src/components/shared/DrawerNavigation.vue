<template>
  <div class="relative z-[60]">
    <transition
      enter-active-class="transition-opacity ease-linear duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity ease-linear duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 bg-black/50 backdrop-blur-sm"
        @click="closeDrawer"
      ></div>
    </transition>

    <transition
      enter-active-class="transition ease-in-out duration-300 transform"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition ease-in-out duration-300 transform"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <div
        v-if="modelValue"
        class="fixed top-0 right-0 h-full w-64 bg-white shadow-2xl p-6 flex flex-col text-left"
      >
        <div class="flex justify-between items-center mb-8 border-b border-gray-100 pb-4">
          <h2 class="text-xl font-bold text-[#008659]">導航選單</h2>
          <button @click="closeDrawer" class="text-gray-400 hover:text-gray-600 transition">
            <SvgItem name="x" size="6" />
          </button>
        </div>

        <nav class="flex-grow space-y-2 w-full">
          <template v-if="currentRole === 'guest'">
            <a @click="$emit('go-team')" class="nav-item">
              <SvgItem name="heart-hand" size="5" />
              <span>開發團隊</span>
            </a>
            <a @click="$emit('go-login')" class="nav-item text-[#008659] bg-green-50">
              <SvgItem name="login" size="5" />
              <span>登入 / 註冊</span>
            </a>
          </template>

          <template v-else-if="currentRole === 'user'">
            <a @click="$emit('go-home')" class="nav-item">
              <SvgItem name="location-dot" size="5" />
              <span>回到地圖</span>
            </a>
            <a @click="$emit('go-history')" class="nav-item">
              <SvgItem name="history" size="5" />
              <span>邀約歷史</span>
            </a>
            <a @click="$emit('go-profile')" class="nav-item">
              <SvgItem name="user" size="5" />
              <span>我的帳戶</span>
            </a>
            <a @click="$emit('go-team')" class="nav-item">
              <SvgItem name="heart-hand" size="5" />
              <span>開發團隊</span>
            </a>
          </template>

          <template v-else-if="currentRole === 'admin'">
            <div class="text-sm text-gray-400 px-0 mb-2 font-bold">管理員功能</div>
            <a class="nav-item opacity-50 cursor-not-allowed">
              <SvgItem name="users" size="5" />
              <span>會員管理</span>
            </a>
          </template>
        </nav>

        <div v-if="currentRole !== 'guest'" class="pt-4 border-t border-gray-100 w-full">
          <a @click="$emit('logout')" class="nav-item text-red-500 hover:bg-red-50">
            <SvgItem name="logout" size="5" />
            <span>登出系統</span>
          </a>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import SvgItem from '@/components/icons/SvgItem.vue'

defineProps<{
  modelValue: boolean
  currentRole: string
}>()

const emit = defineEmits([
  'update:modelValue',
  'go-home',
  'go-login',
  'go-history',
  'go-team',
  'go-profile',
  'logout',
])

const closeDrawer = () => {
  emit('update:modelValue', false)
}
</script>

<style scoped>
/* 【修改重點】
  1. -mx-4: 讓背景往左拉出 1rem (抵銷父層的部分 padding)
  2. w-[calc(100%+2rem)]: 補回被拉出的寬度，讓背景填滿
  3. px-4: 保持內容內縮 1rem，這樣圖示就會剛好回到與標題對齊的位置
*/
.nav-item {
  @apply -mx-4 w-[calc(100%+2rem)] flex items-center justify-start gap-3 px-4 py-3 rounded-lg text-gray-700 font-bold cursor-pointer transition-colors hover:bg-gray-100;
}
</style>
