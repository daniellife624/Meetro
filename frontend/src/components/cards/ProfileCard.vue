<template>
  <div class="relative pt-8 w-full max-w-5xl mx-auto">
    <div class="absolute top-2 left-1/2 transform -translate-x-1/2 z-10">
      <div
        class="bg-[#008659] text-white px-10 py-2 rounded-full text-lg font-bold tracking-widest shadow-sm"
      >
        個人資料
      </div>
    </div>

    <div
      class="bg-white border-[2.5px] border-[#008659] rounded-[30px] px-4 py-10 md:p-12 shadow-sm"
    >
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div
          class="flex flex-col items-center md:items-start px-4 md:border-r-2 md:border-dashed md:border-gray-300"
        >
          <h3 class="text-2xl font-bold text-[#008659] mb-8 w-full text-center">個人基本資料</h3>

          <div class="space-y-6 w-full max-w-xs text-gray-800 font-bold text-lg">
            <div class="flex items-start">
              <span class="w-20 flex-shrink-0 text-right mr-2">姓名 :</span>
              <span>{{ user.name }}</span>
            </div>
            <div class="flex items-start">
              <span class="w-20 flex-shrink-0 text-right mr-2">生日 :</span>
              <span>{{ user.birthday }}</span>
            </div>
            <div class="flex items-start">
              <span class="w-20 flex-shrink-0 text-right mr-2">性別 :</span>
              <span>{{ user.gender }}</span>
            </div>
          </div>
        </div>

        <div
          class="flex flex-col items-center md:items-start px-4 md:border-r-2 md:border-dashed md:border-gray-300"
        >
          <h3 class="text-2xl font-bold text-[#008659] mb-8 w-full text-center">帳戶資料</h3>

          <div class="space-y-8 w-full max-w-xs text-gray-800 font-bold text-lg">
            <div class="flex flex-col xl:flex-row xl:items-start gap-1">
              <span class="flex-shrink-0 xl:text-right xl:mr-2">帳號 :</span>
              <span class="text-base break-all pt-0.5">{{ user.email }}</span>
            </div>

            <div>
              <button
                @click="$emit('change-password')"
                class="text-gray-800 hover:text-[#008659] transition-colors font-bold flex items-center gap-2 group"
              >
                修改密碼
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 opacity-0 group-hover:opacity-100 transition-opacity transform -translate-x-2 group-hover:translate-x-0"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div class="flex flex-col items-center px-4">
          <h3 class="text-2xl font-bold text-[#008659] mb-8 text-center">模擬次數 & 成功機率</h3>

          <div class="flex flex-col items-center justify-start space-y-8 w-full">
            <div class="text-center">
              <p class="text-gray-600 font-bold text-lg mb-1">目前已模擬</p>
              <div class="flex items-baseline justify-center gap-2">
                <span class="text-5xl font-extrabold text-[#008659] leading-none">{{
                  user.simulationCount
                }}</span>
                <span class="text-xl font-bold text-gray-800">次</span>
              </div>
            </div>

            <div class="text-center">
              <p class="text-gray-600 font-bold text-lg mb-1">成功機率約</p>
              <div class="flex items-baseline justify-center gap-1">
                <span class="text-6xl font-extrabold text-[#008659] leading-none">{{
                  user.successRate
                }}</span>
                <span class="text-4xl font-extrabold text-[#008659]">%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface UserProfile {
  name: string
  birthday: string
  gender: string
  email: string
  simulationCount: number
  successRate: number
}

defineProps<{
  user: UserProfile
}>()

defineEmits<{
  (e: 'change-password'): void
}>()
</script>

<style scoped></style>
