<template>
  <!-- 修正 1: 確保兩側都能垂直拉伸 -->
  <div class="flex flex-col md:flex-row h-screen w-full bg-[#f1f8e9] overflow-hidden font-sans">
    <!-- 左側：步驟指南 -->
    <div
      class="w-full md:w-1/3 bg-white border-r border-gray-200 p-6 flex flex-col overflow-y-auto max-h-full md:max-h-screen"
    >
      <h1 class="text-2xl font-extrabold mb-4 text-[#286047] border-b-2 border-[#E8F5E9] pb-3">
        Meetro 發送方步驟指南
      </h1>
      <div class="intro-cards-scroll-area flex-grow overflow-y-auto pr-3">
        <div class="space-y-6">
          <!-- 假設 MeetroIntroCard 在 components/cards/ 路徑下 -->
          <MeetroIntroCard
            v-for="(content, index) in introContents"
            :key="index"
            :text="content"
            :step="index + 1"
          />
        </div>
      </div>
    </div>

    <!-- 右側：發送邀約表單區域 -->
    <div class="flex flex-col w-full md:w-2/3 p-6 relative overflow-y-auto bg-white h-full">
      <h2 class="text-3xl font-extrabold text-[#286047] mb-6 border-b pb-3">
        <!-- 修正: 使用更友善的預設名稱 -->
        發送新邀約：{{ stationName }}站
      </h2>

      <!-- 表單容器 -->
      <div class="space-y-6 flex-grow">
        <!-- 1. 【事】邀約事件 (Title & Description) -->
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

        <!-- 2. 【時】邀約時間 -->
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

        <!-- 3. 【地】地圖區域 (使用 Google Maps API) -->
        <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg shadow-sm">
          <label class="block text-lg font-semibold text-[#1b5e20] mb-2"> 【地】邀約地點 </label>

          <!-- 地點輸入 (使用 Google Places Autocomplete) -->
          <input
            id="autocomplete-input"
            type="text"
            v-model="invitation.locationName"
            placeholder="請輸入或在地圖上點擊來選擇地點"
            class="w-full p-3 mb-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#286047] focus:border-transparent transition-colors"
          />

          <!-- Google Map 容器 -->
          <div id="map" class="w-full h-96 rounded-lg shadow-md border-2 border-[#286047]"></div>

          <!-- 顯示選定的經緯度 (可選，用於確認) -->
          <p class="text-sm text-gray-600 mt-2">
            選定座標：
            <span class="font-mono text-xs text-red-600">{{ invitation.latLng }}</span>
          </p>
        </div>
      </div>

      <!-- 發送按鈕 -->
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, onMounted } from 'vue'
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'

const stationMap: Record<string, string> = {
  xindian: '新店',
  gongguan: '公館',
  nanjingfuxing: '南京復興',
  songshan: '松山',
}

// Google Maps 相關變數
declare const google: any // 宣告 google 變數
let map: any
let marker: any

interface Props {
  station: string // 路由傳入的英文 Key
}
const props = defineProps<Props>()

const stationName = computed(() => {
  // 將 props.station 轉換為小寫，並移除前後空白
  const key = props.station?.toLowerCase().trim() ?? ''

  // 檢查 key 是否為空。如果是空字串（例如路由沒有參數），則提供一個預設的描述性名稱
  if (!key) {
    return '松山新店線任一站'
  }

  // 查閱站名，如果查無結果，則顯示「未知站」
  return stationMap[key] || '未知站'
})

// 狀態：管理邀約表單
const invitation = ref({
  title: '',
  time: '', // datetime-local 格式 'YYYY-MM-DDTHH:MM'
  locationName: '', // 地點名稱
  latLng: '', // 經緯度 'lat,lng'
  // 即使 stationKey 為空，也儲存原始 props.station，但在地圖初始化時會使用預設值
  stationKey: props.station,
})

// 步驟指南內容定義
const introContents = ref<string[]>([
  'STEP 1: 選擇捷運站\n選擇松山新店線(綠線)想探索的捷運站。',
  'STEP 2: 確認目的\n1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
  'STEP 3: 發送方發送邀約\n點選該捷運站後，即會跳出輸入欄位完成邀約目的（事）、邀約時間（時）、邀約地點（地），即可立即發送邀約',
  'STEP 4: 填寫滿意度\n完成邀約後，系統會引導您填寫本次體驗的滿意度，以便優化配對服務。',
  'STEP 5: 成功配對\n當雙方確認並完成所有步驟後，恭喜您！邀約成功，準備出發吧！',
])

// 表單驗證
const isFormValid = computed(() => {
  return (
    invitation.value.title.trim() !== '' &&
    invitation.value.time !== '' &&
    invitation.value.latLng !== '' // 必須選擇地點
  )
})

/**
 * 初始化 Google Map (必須為全域函式以供 Google Maps API 呼叫)
 */
const initMap = () => {
  // 將 initialCoords 的 Key 全部改為小寫
  const initialCoords: Record<string, { lat: number; lng: number }> = {
    gongguan: { lat: 25.0135, lng: 121.5365 },
    xindian: { lat: 24.9491, lng: 121.5422 },
    nanjingfuxing: { lat: 25.0526, lng: 121.5435 },
    songshan: { lat: 25.0504, lng: 121.5732 },
  }

  // 將 props.station 轉換為小寫並移除空格來查閱座標，預設為 'gongguan'
  const stationKey = props.station?.toLowerCase().trim() ?? 'gongguan'
  // 如果 stationKey 無效，則使用 'gongguan' 作為中心點
  const center = initialCoords[stationKey] || initialCoords['gongguan']

  // 2. 創建地圖
  map = new google.maps.Map(document.getElementById('map') as HTMLElement, {
    center: center,
    zoom: 15,
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: false,
  })

  // 3. 創建標記
  marker = new google.maps.Marker({
    position: center,
    map: map,
    title: stationName.value,
  })

  // 初始化地點名稱和經緯度
  invitation.value.locationName = stationName.value + '捷運站周邊'
  invitation.value.latLng = `${center.lat},${center.lng}`

  // 4. 設定地點自動完成 (Autocomplete)
  const input = document.getElementById('autocomplete-input') as HTMLInputElement
  const autocomplete = new google.maps.places.Autocomplete(input)
  autocomplete.bindTo('bounds', map)

  autocomplete.addListener('place_changed', () => {
    const place = autocomplete.getPlace()
    if (!place.geometry) {
      console.warn('Place not found or has no geometry:', place.name)
      return
    }

    // 更新地圖視圖
    map.setCenter(place.geometry.location)
    map.setZoom(17)

    // 更新標記位置
    marker.setPosition(place.geometry.location)

    // 更新邀約資料
    invitation.value.locationName = place.name || ''
    invitation.value.latLng = `${place.geometry.location.lat()},${place.geometry.location.lng()}`
    console.log('[Map] 地點已透過搜尋選擇:', invitation.value.locationName)
  })

  // 5. 點擊地圖選擇地點
  map.addListener('click', (e: any) => {
    // 更新標記位置
    marker.setPosition(e.latLng)

    // 進行反向地理編碼 (Reverse Geocoding)
    const geocoder = new google.maps.Geocoder()
    geocoder.geocode({ location: e.latLng }, (results: any, status: any) => {
      if (status === 'OK' && results[0]) {
        invitation.value.locationName = results[0].formatted_address || '地圖點擊位置'
      } else {
        invitation.value.locationName = '地圖點擊位置'
        console.warn('Reverse Geocode failed due to: ' + status)
      }

      // 更新邀約資料
      invitation.value.latLng = `${e.latLng.lat()},${e.latLng.lng()}`
      console.log('[Map] 地點已透過地圖點擊選擇:', invitation.value.locationName)
    })
  })
}

/**
 * 模擬發送邀約邏輯
 */
const sendInvitation = () => {
  if (!isFormValid.value) {
    console.warn('[Validation] 請填寫完整的邀約資訊 (主題、時間、地點)。')
    // TODO: 請使用自定義的 Modal UI 來顯示錯誤訊息，避免使用 window.alert()
    return
  }

  // 模擬發送資料
  const inviteData = {
    ...invitation.value,
    createdAt: new Date().toISOString(),
    status: 'pending',
  }

  console.log('[Data Operation] 準備發送邀約資料 (模擬):', inviteData)

  // 實作發送到後端的邏輯，這裡使用 console.log 替代
  console.log('--- 模擬邀約已發送！ ---')
  console.log(`發送站點 Key: ${inviteData.stationKey}, 中文站名: ${stationName.value}`)
  console.log(`邀約標題: ${inviteData.title}`)
  console.log(`邀約時間: ${inviteData.time}`)
  console.log(`邀約地點: ${inviteData.locationName} (座標: ${inviteData.latLng})`)
  console.log('---------------------------')

  // TODO: 成功後導航到等待配對的頁面，並使用 Custom Modal 顯示成功訊息

  // 清空表單 (可選)
  invitation.value.title = ''
  invitation.value.time = ''
  invitation.value.locationName = ''
  invitation.value.latLng = ''
}

// 將 initMap 函式暴露給 window，讓 Google Maps API 載入完成後可以呼叫
;(window as any).initMap = initMap

onMounted(() => {
  // 載入 Google Maps API
  const script = document.createElement('script')
  // 注意：實際應用中，您需要替換為您的 Google Maps API Key
  script.src =
    'https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE&libraries=places&callback=initMap'
  script.async = true
  script.defer = true
  document.head.appendChild(script)
})
</script>

<style scoped>
/* 隱藏 datetime-local 的部分瀏覽器預設箭頭 */
input[type='datetime-local']::-webkit-calendar-picker-indicator {
  cursor: pointer;
}

/* 確保時間選擇器能夠選到分鐘 */
input[type='datetime-local'] {
  min-height: 3.5rem; /* 增加高度，使其更易點擊 */
}

/* 滾動條樣式 */
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
