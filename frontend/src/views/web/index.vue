<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-gray-100 overflow-hidden font-sans">
    <div
      class="w-full md:w-1/3 bg-white border-r border-gray-200 p-6 flex flex-col overflow-y-auto max-h-full md:max-h-screen"
    >
      <h1 class="text-2xl font-extrabold mb-4 text-[#008659] border-b-2 border-[#E8F5E9] pb-3">
        Meetro 步驟指南
      </h1>
      <div class="intro-cards-scroll-area flex-grow overflow-y-auto pr-3">
        <div class="space-y-4">
          <MeetroIntroCard
            v-for="(step, index) in introSteps"
            :key="index"
            :step-number="index + 1"
            :title="step.title"
            :content="step.content"
            :icon-name="step.icon"
          />
        </div>
      </div>
    </div>

    <div class="flex flex-col w-full md:w-2/3 p-6 relative overflow-y-auto">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
        <h1 class="text-3xl font-extrabold text-[#008659] mb-3 sm:mb-0">捷運 松山新店線 地圖</h1>

        <div class="flex gap-3">
          <button
            @click="goToEmaWall"
            class="px-5 py-2 bg-white text-[#008659] border-2 border-[#008659] font-bold rounded-full shadow hover:bg-green-50 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            :disabled="!selectedStationKey"
          >
            <span> {{ selectedStationName }} 繪馬牆</span>
          </button>

          <button
            @click="openPopup"
            class="px-6 py-2 bg-[#008659] text-white font-bold rounded-full shadow-lg hover:bg-green-700 transition duration-300 disabled:bg-gray-400 disabled:cursor-not-allowed"
            :disabled="!selectedStationKey"
          >
            開始探索 {{ selectedStationName }}站
          </button>
        </div>
      </div>

      <div
        class="flex-grow bg-[#E8F5E9] border border-[#C8E6C9] rounded-xl shadow-inner mb-6 flex items-start justify-center relative min-h-[300px] p-4 pt-10"
      >
        <div class="text-center w-full space-y-6">
          <p class="text-xl font-semibold text-[#008659]">點擊下方站點來選擇您想探索的地點</p>

          <div class="w-full max-w-5xl mx-auto">
            <div class="relative w-full">
              <div
                class="absolute top-1/2 left-0 right-0 h-2 bg-[#008659] transform -translate-y-1/2 z-0"
              ></div>
              <div class="flex justify-between items-start relative z-10 px-4">
                <div
                  v-for="key in line1Keys"
                  :key="key"
                  class="flex flex-col items-center flex-shrink-0"
                >
                  <span
                    @click="selectStation(key)"
                    :class="{
                      'bg-yellow-300 text-gray-800 font-extrabold ring-4 ring-white ring-offset-2 ring-offset-[#008659] shadow-xl scale-125':
                        key === selectedStationKey,
                      'bg-white text-[#008659] cursor-pointer hover:bg-green-100':
                        key !== selectedStationKey,
                    }"
                    class="w-12 h-12 flex items-center justify-center rounded-full text-sm transition duration-150 transform hover:scale-110 font-bold border-2 border-[#008659] shadow-md flex-shrink-0 z-10 mb-2"
                  >
                    {{ stationMap[key].slice(0, 2) }}
                  </span>
                  <p
                    class="text-xs text-gray-700 font-medium whitespace-nowrap pt-1"
                    :class="{ 'font-bold text-[#008659]': key === selectedStationKey }"
                  >
                    {{ stationMap[key] }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="w-full max-w-5xl mx-auto">
            <div class="relative w-full">
              <div
                class="absolute top-1/2 left-0 right-0 h-2 bg-[#008659] transform -translate-y-1/2 z-0"
              ></div>
              <div class="flex justify-between items-start relative z-10 px-4">
                <div
                  v-for="key in line2Keys"
                  :key="key"
                  class="flex flex-col items-center flex-shrink-0 relative"
                >
                  <span
                    @click="selectStation(key)"
                    :class="{
                      'bg-yellow-300 text-gray-800 font-extrabold ring-4 ring-white ring-offset-2 ring-offset-[#008659] shadow-xl scale-125':
                        key === selectedStationKey,
                      'bg-white text-[#008659] cursor-pointer hover:bg-green-100':
                        key !== selectedStationKey,
                    }"
                    class="w-12 h-12 flex items-center justify-center rounded-full text-sm transition duration-150 transform hover:scale-110 font-bold border-2 border-[#008659] shadow-md flex-shrink-0 z-10 mb-2"
                  >
                    {{ stationMap[key].slice(0, 2) }}
                  </span>
                  <p
                    class="text-xs text-gray-700 font-medium whitespace-nowrap pt-1"
                    :class="{ 'font-bold text-[#008659]': key === selectedStationKey }"
                  >
                    {{ stationMap[key] }}
                  </p>

                  <template v-if="key === branchStartKey">
                    <div
                      class="absolute top-full mt-3 flex flex-col items-center z-10"
                      style="transform: translateX(0px)"
                    >
                      <div class="w-0.5 h-6 bg-[#008659]"></div>
                      <span
                        @click="selectStation(branchLineKey)"
                        :class="{
                          'bg-yellow-300 text-gray-800 font-extrabold ring-4 ring-white ring-offset-2 ring-offset-[#cfdb00] shadow-xl scale-125':
                            branchLineKey === selectedStationKey,
                          'bg-white text-[#cfdb00] cursor-pointer hover:bg-green-100':
                            branchLineKey !== selectedStationKey,
                        }"
                        class="w-12 h-12 flex items-center justify-center rounded-full text-sm transition duration-150 transform hover:scale-110 font-bold border-2 border-[#cfdb00] shadow-md flex-shrink-0 z-10 mb-2"
                      >
                        {{ stationMap[branchLineKey].slice(0, 2) }}
                      </span>
                      <p
                        class="text-xs text-gray-700 font-medium whitespace-nowrap pt-1"
                        :class="{
                          'font-bold text-[#008659]': branchLineKey === selectedStationKey,
                        }"
                      >
                        {{ stationMap[branchLineKey] }}
                      </p>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex flex-col md:flex-row items-stretch gap-5">
        <div
          class="bg-white p-4 rounded-xl shadow-lg border border-gray-200 w-full md:w-1/2 text-sm space-y-2"
        >
          <p class="font-bold text-[#008659]">
            目前選擇捷運站：<span class="text-red-500 font-extrabold">{{
              selectedStationName
            }}</span>
          </p>
          <p class="text-gray-700">知名景點：{{ getAttractions(selectedStationKey) }}</p>
        </div>
        <div
          class="bg-white p-4 rounded-xl shadow-lg border border-gray-200 w-full md:w-1/2 text-sm space-y-2"
        >
          <p class="text-gray-700">天氣：{{ weatherData }}</p>
        </div>
      </div>
    </div>

    <PopupBoxLayout
      v-if="showExplorePopup"
      title="選擇探索角色"
      confirm-text="挑選景點"
      :cancel-callback="closePopup"
      :confirm-callback="() => {}"
      type="normal"
      :use-form="false"
      id="explore-station-popup"
      class="popup-box-explore"
    >
      <ExploreStationPopup
        :selected-station="selectedStationKey"
        @explore="handleExploreConfirmed"
      />
    </PopupBoxLayout>

    <PopupBoxLayout
      v-if="showLoginHint"
      title="會員專屬服務"
      :cancel-callback="closeLoginHint"
      :use-form="false"
      id="login-hint-popup"
    >
      <LoginHintPopup @go-login="handleGoToLogin" @cancel="closeLoginHint" />
    </PopupBoxLayout>

    <div
      v-if="customAlert"
      class="fixed top-5 right-5 z-[100] bg-white text-[#008659] p-4 rounded-lg shadow-xl border-t-4 border-[#008659] transition-opacity duration-500 animate-fadeInOut"
    >
      {{ customAlert }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRoleStore } from '@/stores/modules/useRole'
import request from '@/utils/request'

// Components
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'
import PopupBoxLayout from '@/components/web/PopupBox/PopupBoxLayout.vue'
import ExploreStationPopup from '@/components/web/PopupBox/ExploreStationPopup.vue'
import LoginHintPopup from '@/components/web/PopupBox/LoginHintPopup.vue'

const router = useRouter()
const roleStore = useRoleStore()

// --- 地圖資料與邏輯 ---

const stationMap: Record<string, string> = {
  songshan: '松山',
  nanjingsanmin: '南京三民',
  taipeiarena: '台北小巨蛋',
  nanjingfuxing: '南京復興',
  songjiangnanjing: '松江南京',
  zhongshan: '中山',
  beimen: '北門',
  ximen: '西門',
  xiaonanmen: '小南門',
  chiangkaishekmemorialhall: '中正紀念堂',
  guting: '古亭',
  taipowerbuilding: '台電大樓',
  gongguan: '公館',
  wanlong: '萬隆',
  jingmei: '景美',
  dapinglin: '大坪林',
  qizhang: '七張',
  xiaobitan: '小碧潭',
  xindiandistrictoffice: '新店區公所',
  xindian: '新店',
}

const mainLineKeys: string[] = [
  'songshan',
  'nanjingsanmin',
  'taipeiarena',
  'nanjingfuxing',
  'songjiangnanjing',
  'zhongshan',
  'beimen',
  'ximen',
  'xiaonanmen',
  'chiangkaishekmemorialhall',
  'guting',
  'taipowerbuilding',
  'gongguan',
  'wanlong',
  'jingmei',
  'dapinglin',
  'qizhang',
  'xindiandistrictoffice',
  'xindian',
]

const branchLineKey = 'xiaobitan'
const branchStartKey = 'qizhang'

const line1Keys = computed(() => mainLineKeys.slice(0, 10))
const line2Keys = computed(() => mainLineKeys.slice(10))

const selectedStationKey = ref<string>('songshan')
const showExplorePopup = ref<boolean>(false)
const showLoginHint = ref<boolean>(false)
const weatherData = ref<string>('(抓取天氣API資料)')
const customAlert = ref<string | null>(null)
const currentAttractions = ref<string[]>([])

const selectedStationName = computed(() => stationMap[selectedStationKey.value] || '')

const stationAttractions: Record<string, string> = {
  songshan: '饒河街夜市、松山慈祐宮、五分埔',
  nanjingsanmin: '小巨蛋、東方文華酒店',
  taipeiarena: '台北小巨蛋、育達高職',
  nanjingfuxing: '微風廣場、遼寧夜市、慶城街',
  songjiangnanjing: '四平陽光商圈、袖珍博物館',
  zhongshan: '中山商圈、新光三越、光點台北',
  beimen: '北門、台北郵局、承恩門',
  ximen: '西門町、紅樓、萬年商業大樓',
  xiaonanmen: '植物園、歷史博物館',
  chiangkaishekmemorialhall: '中正紀念堂、國家戲劇院、國家音樂廳',
  guting: '客家文化主題公園、師大夜市',
  taipowerbuilding: '台電大樓、古亭河濱公園',
  gongguan: '國立臺灣大學、水源市場、寶藏巖',
  wanlong: '萬隆變電所、景美溪河濱公園',
  jingmei: '景美夜市、仙跡岩步道',
  dapinglin: '大坪林、新店家樂福',
  qizhang: '七張、裕隆城',
  xiaobitan: '小碧潭、新店溪河濱公園',
  xindiandistrictoffice: '新店區公所、瑠公公園',
  xindian: '碧潭風景區、新店老街、和美山步道',
}

// --- 步驟指南資料 (寫死、使用 String Icon Name) ---
// 這裡直接傳遞 SvgItem 的 name 字串，乾淨俐落
const introSteps = [
  {
    title: 'STEP 1: 選擇捷運站',
    content: '選擇松山新店線(綠線)想探索的捷運站。',
    icon: 'location-dot', // 对应 map-pin
  },
  {
    title: 'STEP 2: 確認目的',
    content: '1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
    icon: 'target',
  },
  {
    title: 'STEP 3: 發送邀約 / 選擇邀約',
    content: '此部分將根據 邀約發送方 or 邀約選擇方 而有不同操作方式。',
    icon: 'send',
  },
  {
    title: 'STEP 4: 填寫滿意度',
    content: '完成邀約後，系統會引導您填寫本次體驗的滿意度，以便優化配對服務。',
    icon: 'check',
  },
  {
    title: 'STEP 5: 成功配對',
    content: '當雙方確認並完成所有步驟後，恭喜您！邀約成功，準備出發吧！',
    icon: 'party',
  },
]

// --- Functions ---

const showAlert = (message: string) => {
  customAlert.value = message
  setTimeout(() => {
    customAlert.value = null
  }, 3000)
}

const selectStation = async (key: string) => {
  selectedStationKey.value = key

  weatherData.value = '連線後端中...'
  currentAttractions.value = [] // 清空舊景點

  try {
    // 呼叫後端 API
    const res: any = await request.get(`/api/stations/${key}`)

    console.log('後端回傳:', res)

    // 更新資料
    if (res.weather) {
      weatherData.value = res.weather
    }
    if (res.attractions) {
      currentAttractions.value = res.attractions
    }
  } catch (error) {
    console.error(error)
    weatherData.value = '連線失敗 (請確認後端是否啟動)'
  }
}

const getAttractions = (key: string): string => {
  // 如果有 API 回傳的資料，優先顯示
  if (currentAttractions.value.length > 0) {
    return currentAttractions.value.join('、')
  }

  // 如果正在載入中 (weatherData 顯示連線中)，顯示載入提示
  if (weatherData.value === '連線後端中...') {
    return '資料讀取中...'
  }

  // 否則顯示前端寫死的靜態資料 (作為備案)
  return stationAttractions[key] || '無已知景點'
}

const openPopup = () => {
  if (roleStore.isGuest) {
    showLoginHint.value = true
  } else {
    showExplorePopup.value = true
  }
}

const closePopup = () => {
  showExplorePopup.value = false
}
const closeLoginHint = () => {
  showLoginHint.value = false
}

const handleGoToLogin = () => {
  closeLoginHint()
  router.push({ name: 'WebLogin' })
}

const handleExploreConfirmed = (key: string, role: 'sender' | 'receiver') => {
  closePopup()
  const routeName = role === 'sender' ? 'SenderView' : 'ReceiverView'
  try {
    router.push({ name: routeName, params: { stationKey: key } })
  } catch (error: any) {
    console.error(error)
    showAlert('導航失敗，請檢查路由配置')
  }
}

const goToEmaWall = () => {
  if (selectedStationKey.value) {
    router.push({
      name: 'EmaWall',
      params: { stationKey: selectedStationKey.value },
    })
  }
}
</script>

<style scoped>
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
@keyframes fadeInOut {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  5% {
    opacity: 1;
    transform: translateY(0);
  }
  95% {
    opacity: 1;
    transform: translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateY(-10px);
  }
}
.animate-fadeInOut {
  animation: fadeInOut 3s ease-in-out forwards;
}
.whitespace-nowrap {
  white-space: nowrap;
}
</style>
