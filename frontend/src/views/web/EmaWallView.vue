<template>
  <div class="min-h-screen bg-[#F3F4F6] pb-20 font-sans">
    <div class="bg-white shadow-sm sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button @click="$router.back()" class="p-2 hover:bg-gray-100 rounded-full transition">
            <span class="text-xl font-bold text-gray-600">←</span>
          </button>
          <div>
            <h1 class="text-xl font-bold text-[#286047]">{{ stationName }} 繪馬牆</h1>
            <p class="text-xs text-gray-500">看看大家在這裡留下了什麼回憶...</p>
          </div>
        </div>

        <button
          @click="openCreateModal"
          class="hidden md:flex items-center gap-2 bg-[#286047] text-white px-4 py-2 rounded-full font-bold hover:bg-[#1e4a36] transition shadow-md"
        >
          <span class="text-xl">+</span> 寫繪馬
        </button>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <div class="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-6 space-y-6">
        <EmaCard v-for="ema in emaList" :key="ema.id" :ema="ema" />
      </div>
      <div v-if="emaList.length === 0" class="text-center py-20 text-gray-400">
        <p class="text-lg">目前還沒有人掛上繪馬，成為第一個吧！</p>
      </div>
    </div>

    <button
      @click="openCreateModal"
      class="md:hidden fixed bottom-8 right-6 w-14 h-14 bg-[#286047] text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-110 transition-transform z-20"
    >
      <span class="text-3xl font-light pb-1">+</span>
    </button>

    <PopupBoxLayout
      v-if="showCreateModal"
      title="掛上新繪馬"
      :cancel-callback="() => (showCreateModal = false)"
      :use-form="false"
    >
      <CreateEmaPopup @cancel="showCreateModal = false" @submit="submitEma" />
    </PopupBoxLayout>

    <PopupBoxLayout
      v-if="showLoginHint"
      title="會員專屬服務"
      :cancel-callback="() => (showLoginHint = false)"
    >
      <LoginHintPopup @go-login="handleGoToLogin" @cancel="() => (showLoginHint = false)" />
    </PopupBoxLayout>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRoleStore } from '@/stores/modules/useRole'
import EmaCard, { type EmaItem } from '@/components/cards/EmaCard.vue'
import PopupBoxLayout from '@/components/web/PopupBox/PopupBoxLayout.vue'
import LoginHintPopup from '@/components/web/PopupBox/LoginHintPopup.vue'
import CreateEmaPopup from '@/components/web/PopupBox/CreateEmaPopup.vue'

const props = defineProps<{ stationKey: string }>()
const router = useRouter()
const roleStore = useRoleStore()

const stationMap: Record<string, string> = { songshan: '松山', gongguan: '公館' }
const stationName = computed(() => stationMap[props.stationKey?.toLowerCase()] || props.stationKey)
const showCreateModal = ref(false)
const showLoginHint = ref(false)
const allEmas = ref([
  {
    id: 1,
    station: 'gongguan',
    userName: '小明',
    location: '寶藏巖',
    content: '很美',
    photoUrl: '...',
    date: '2025/02/14',
  },
])
const emaList = computed(
  () => allEmas.value.filter((ema) => ema.station === props.stationKey?.toLowerCase()) as EmaItem[],
)

const openCreateModal = () => {
  if (roleStore.isGuest) {
    showLoginHint.value = true
  } else {
    showCreateModal.value = true
  }
}

const handleGoToLogin = () => {
  showLoginHint.value = false
  router.push({ name: 'WebLogin' })
}

const submitEma = (data: { location: string; content: string; photoUrl: string }) => {
  alert('發佈成功！(模擬)')
  showCreateModal.value = false

  allEmas.value.unshift({
    id: Date.now(),
    station: props.stationKey.toLowerCase(),
    userName: '我',
    location: data.location,
    content: data.content,
    photoUrl: data.photoUrl,
    date: new Date().toLocaleDateString(),
  })
}
</script>
