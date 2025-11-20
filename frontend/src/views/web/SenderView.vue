<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-[#f1f8e9] overflow-hidden font-sans">
    <div
      class="w-full md:w-1/3 bg-white border-r border-gray-200 p-6 flex flex-col overflow-y-auto max-h-full md:max-h-screen"
    >
      <h1 class="text-2xl font-extrabold mb-4 text-[#286047] border-b-2 border-[#E8F5E9] pb-3">
        Meetro 發送方步驟指南
      </h1>
      <div class="intro-cards-scroll-area flex-grow overflow-y-auto pr-3">
        <div class="space-y-6">
          <MeetroIntroCard
            v-for="(content, index) in introContents"
            :key="index"
            :text="content"
            :step="index + 1"
          />
        </div>
      </div>
    </div>

    <div class="flex flex-col w-full md:w-2/3 p-6 relative overflow-y-auto bg-white h-full">
      <h2 class="text-3xl font-extrabold text-[#286047] mb-6 border-b pb-3">
        發送新邀約：{{ stationName }}站
      </h2>

      <div class="space-y-6 flex-grow">
        <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg shadow-sm">
          <label for="invite-title" class="block text-lg font-semibold text-[#1b5e20] mb-2">
            【事】邀約主題 <span class="text-red-500">*</span>
          </label>
          <textarea
            id="invite-title"
            v-model="invitation.title"
            rows="3"
            placeholder="請簡述您的邀約內容 (例如：在綠線XX站附近找人一起打電動、看展覽...)"
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#286047] focus:border-transparent transition-colors resize-none"
            maxlength="50"
          ></textarea>
          <p class="text-right text-xs text-gray-500 mt-1">{{ invitation.title.length }} / 50 字</p>
        </div>

        <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg shadow-sm">
          <label for="invite-time" class="block text-lg font-semibold text-[#1b5e20] mb-2">
            【時】邀約時間 <span class="text-red-500">*</span>
          </label>
          <input
            id="invite-time"
            type="datetime-local"
            v-model="invitation.time"
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#286047] focus:border-transparent transition-colors"
          />
        </div>

        <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg shadow-sm">
          <label class="block text-lg font-semibold text-[#1b5e20] mb-2"> 【地】邀約地點 </label>

          <input
            id="autocomplete-input"
            type="text"
            v-model="invitation.locationName"
            placeholder="請輸入或在地圖上點擊來選擇地點"
            class="w-full p-3 mb-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#286047] focus:border-transparent transition-colors"
          />

          <div id="map" class="w-full h-96 rounded-lg shadow-md border-2 border-[#286047]"></div>

          <p class="text-sm text-gray-600 mt-2">
            選定座標：<span class="font-mono text-xs text-red-600">{{ invitation.latLng }}</span>
          </p>
        </div>
      </div>

      <div class="flex justify-end items-center pt-6 border-t border-gray-200 mt-6">
        <button
          @click="sendInvitation"
          :disabled="!isFormValid"
          class="bg-[#008659] text-white font-bold px-12 py-3 rounded-full hover:bg-green-700 transition-colors disabled:bg-gray-400 shadow-xl"
        >
          發送邀約
        </button>
      </div>
    </div>

    <div
      v-if="showSuccessModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-filter backdrop-blur-sm"
    >
      <div
        class="bg-white rounded-2xl p-8 max-w-sm w-full mx-4 shadow-2xl text-center transform transition-all scale-100"
      >
        <div
          class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4"
        >
          <svg class="w-8 h-8 text-[#286047]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="3"
              d="M5 13l4 4L19 7"
            ></path>
          </svg>
        </div>
        <h3 class="text-xl font-extrabold text-gray-800 mb-2">邀約發送成功！</h3>
        <p class="text-gray-600 mb-6">
          您的邀約已發布到 {{ stationName }} 站，等待有緣人與您聯繫。
        </p>
        <div class="space-y-3">
          <button
            @click="goHome"
            class="w-full py-3 bg-[#286047] text-white font-bold rounded-xl hover:bg-green-800 transition"
          >
            回到首頁
          </button>
          <button
            @click="showSuccessModal = false"
            class="w-full py-3 text-gray-500 font-bold rounded-xl hover:bg-gray-100 transition"
          >
            繼續留在本頁
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'

const router = useRouter()

const stationMap: Record<string, string> = {
  xindian: '新店',
  gongguan: '公館',
  nanjingfuxing: '南京復興',
  songshan: '松山',
}

// Google Maps 變數
declare const google: any
let map: any
let marker: any

interface Props {
  stationKey: string
}
const props = defineProps<Props>()

const stationName = computed(() => {
  const key = props.stationKey?.toLowerCase().trim() ?? ''
  if (!key) return '松山新店線任一站'
  return stationMap[key] || '未知站'
})

const invitation = ref({
  title: '',
  time: '',
  locationName: '',
  latLng: '',
  // 【修正重點】這裡改成 props.stationKey
  stationKey: props.stationKey,
})

const showSuccessModal = ref(false)

const introContents = ref<string[]>([
  'STEP 1: 選擇捷運站\n選擇松山新店線(綠線)想探索的捷運站。',
  'STEP 2: 確認目的\n1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
  'STEP 3: 發送方發送邀約\n點選該捷運站後，即會跳出輸入欄位完成邀約目的（事）、邀約時間（時）、邀約地點（地），即可立即發送邀約',
  'STEP 4: 填寫滿意度\n完成邀約後，系統會引導您填寫本次體驗的滿意度，以便優化配對服務。',
  'STEP 5: 成功配對\n當雙方確認並完成所有步驟後，恭喜您！邀約成功，準備出發吧！',
])

const isFormValid = computed(() => {
  return (
    invitation.value.title.trim() !== '' &&
    invitation.value.time !== '' &&
    invitation.value.latLng !== ''
  )
})

const initMap = () => {
  const initialCoords: Record<string, { lat: number; lng: number }> = {
    gongguan: { lat: 25.0135, lng: 121.5365 },
    xindian: { lat: 24.9491, lng: 121.5422 },
    nanjingfuxing: { lat: 25.0526, lng: 121.5435 },
    songshan: { lat: 25.0504, lng: 121.5732 },
  }

  const sKey = props.stationKey?.toLowerCase().trim() ?? 'gongguan'
  const center = initialCoords[sKey] || initialCoords['gongguan']

  map = new google.maps.Map(document.getElementById('map') as HTMLElement, {
    center: center,
    zoom: 15,
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: false,
  })

  marker = new google.maps.Marker({
    position: center,
    map: map,
    title: stationName.value,
  })

  invitation.value.locationName = stationName.value + '捷運站周邊'
  invitation.value.latLng = `${center.lat},${center.lng}`

  const input = document.getElementById('autocomplete-input') as HTMLInputElement
  const autocomplete = new google.maps.places.Autocomplete(input)
  autocomplete.bindTo('bounds', map)

  autocomplete.addListener('place_changed', () => {
    const place = autocomplete.getPlace()
    if (!place.geometry) return

    map.setCenter(place.geometry.location)
    map.setZoom(17)
    marker.setPosition(place.geometry.location)

    invitation.value.locationName = place.name || ''
    invitation.value.latLng = `${place.geometry.location.lat()},${place.geometry.location.lng()}`
  })

  map.addListener('click', (e: any) => {
    marker.setPosition(e.latLng)
    const geocoder = new google.maps.Geocoder()
    geocoder.geocode({ location: e.latLng }, (results: any, status: any) => {
      if (status === 'OK' && results[0]) {
        invitation.value.locationName = results[0].formatted_address || '地圖點擊位置'
      } else {
        invitation.value.locationName = '地圖點擊位置'
      }
      invitation.value.latLng = `${e.latLng.lat()},${e.latLng.lng()}`
    })
  })
}

const sendInvitation = () => {
  if (!isFormValid.value) return

  // 模擬 API 發送資料
  const inviteData = {
    ...invitation.value,
    createdAt: new Date().toISOString(),
    status: 'pending',
  }
  console.log('邀約資料已送出:', inviteData)

  // 顯示成功視窗
  showSuccessModal.value = true

  // 清空表單
  invitation.value.title = ''
  invitation.value.time = ''
  // 地點通常保留使用者上次選擇的位置，體驗較佳
}

const goHome = () => {
  router.push({ name: 'Home' }) // 假設首頁路由名稱為 Home，請依實際狀況調整
}

;(window as any).initMap = initMap

onMounted(() => {
  const script = document.createElement('script')
  // 請記得替換為您的 API Key
  script.src =
    'https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE&libraries=places&callback=initMap'
  script.async = true
  script.defer = true
  document.head.appendChild(script)
})
</script>

<style scoped>
input[type='datetime-local']::-webkit-calendar-picker-indicator {
  cursor: pointer;
}
input[type='datetime-local'] {
  min-height: 3.5rem;
}
.intro-cards-scroll-area::-webkit-scrollbar {
  width: 8px;
}
.intro-cards-scroll-area::-webkit-scrollbar-thumb {
  background-color: #a5d6a7;
  border-radius: 4px;
}
.intro-cards-scroll-area::-webkit-scrollbar-track {
  background: #f3f4f6;
}
</style>
