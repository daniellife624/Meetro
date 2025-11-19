<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-gray-100 overflow-hidden font-sans">
    <!-- 左側：步驟指南 -->
    <div
      class="w-full md:w-1/3 bg-white border-r border-gray-200 p-6 flex flex-col overflow-y-auto max-h-full md:max-h-screen"
    >
      <h1 class="text-2xl font-extrabold mb-4 text-[#286047] border-b-2 border-[#E8F5E9] pb-3">
        Meetro 步驟指南
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

    <!-- 右側：地圖與操作區域 -->
    <div class="flex flex-col w-full md:w-2/3 p-6 relative overflow-y-auto">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
        <h1 class="text-3xl font-extrabold text-[#286047] mb-3 sm:mb-0">捷運 松山新店線 地圖</h1>
        <button
          @click="openPopup"
          class="px-6 py-2 bg-[#286047] text-white font-bold rounded-full shadow-lg hover:bg-green-700 transition duration-300 disabled:bg-gray-400 disabled:cursor-not-allowed"
          :disabled="!selectedStationKey"
        >
          開始探索 {{ selectedStationName }}站
        </button>
      </div>

      <!-- 地圖顯示區域 (兩條線路設計) -->
      <div
        class="flex-grow bg-[#E8F5E9] border border-[#C8E6C9] rounded-xl shadow-inner mb-6 flex items-center justify-center relative min-h-[300px] p-4"
      >
        <div class="text-center w-full space-y-12">
          <p class="text-xl font-semibold text-[#286047]">點擊下方站點來選擇您想探索的地點</p>
          <div class="w-full max-w-5xl mx-auto">
            <div class="relative w-full">
              <div
                class="absolute top-1/2 left-0 right-0 h-2 bg-[#008659] transform -translate-y-1/2 z-0"
              ></div>
              <!-- 站點圓圈 -->
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
                    :class="{ 'font-bold text-[#286047]': key === selectedStationKey }"
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

              <!-- 站點圓圈 -->
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
                    :class="{ 'font-bold text-[#286047]': key === selectedStationKey }"
                  >
                    {{ stationMap[key] }}
                  </p>

                  <!-- 小碧潭支線視覺 (從七張站分支) -->
                  <template v-if="key === branchStartKey">
                    <div
                      class="absolute top-full mt-3 flex flex-col items-center z-10"
                      style="transform: translateX(0px)"
                    >
                      <!-- 支線垂直連線 -->
                      <div class="w-0.5 h-6 bg-[#008659]"></div>
                      <!-- 小碧潭站點 -->
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
                          'font-bold text-[#286047]': branchLineKey === selectedStationKey,
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

      <!-- 底部資訊欄：選定的站點資訊 -->
      <div class="flex flex-col md:flex-row items-stretch gap-5">
        <!-- 左下方：站點景點資訊 -->
        <div
          class="bg-white p-4 rounded-xl shadow-lg border border-gray-200 w-full md:w-1/2 text-sm space-y-2"
        >
          <p class="font-bold text-[#286047]">
            目前選播捷運站：<span class="text-red-500 font-extrabold">{{
              selectedStationName
            }}</span>
          </p>
          <p class="text-gray-700">知名景點：{{ getAttractions(selectedStationKey) }}</p>
        </div>
        <!-- 右下方：天氣資訊 -->
        <div
          class="bg-white p-4 rounded-xl shadow-lg border border-gray-200 w-full md:w-1/2 text-sm space-y-2"
        >
          <p class="text-gray-700">天氣：{{ weatherData }}</p>
        </div>
      </div>
    </div>

    <!-- 彈出視窗組件 (Popup) -->
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

    <!-- 自定義 Alert 訊息 -->
    <div
      v-if="customAlert"
      class="fixed top-5 right-5 z-[100] bg-white text-[#286047] p-4 rounded-lg shadow-xl border-t-4 border-[#286047] transition-opacity duration-500 animate-fadeInOut"
    >
      {{ customAlert }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'
import PopupBoxLayout from '@/components/web/PopupBox/PopupBoxLayout.vue'
import ExploreStationPopup from '@/components/web/PopupBox/ExploreStationPopup.vue'

const router = useRouter()

// 完整的松山新店線站點資訊 (21站)
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
  xiaobitan: '小碧潭', // 支線
  xindiandistrictoffice: '新店區公所',
  xindian: '新店',
}

// 站點主線的實際順序 (排除小碧潭支線)
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
  'chiangkaishekmemorialhall', // Index 9: 第十站 (Line 1 End)
  'guting', // Index 10: 第十一站 (Line 2 Start)
  'taipowerbuilding',
  'gongguan',
  'wanlong',
  'jingmei',
  'dapinglin',
  'qizhang', // Index 16: 七張站 (支線分支點)
  'xindiandistrictoffice',
  'xindian', // Index 18: 最後一站
]

// 支線和分支點的 Key
const branchLineKey = 'xiaobitan'
const branchStartKey = 'qizhang'

// 將主線分成兩條線路 (Line 1: 10站, Line 2: 9站)
const line1Keys = computed(() => mainLineKeys.slice(0, 10)) // 松山 -> 中正紀念堂
const line2Keys = computed(() => mainLineKeys.slice(10)) // 古亭 -> 新店

const selectedStationKey = ref<string>('songshan') // 預設選取松山站
const showExplorePopup = ref<boolean>(false)
const weatherData = ref<string>('(抓取天氣API資料)')
const customAlert = ref<string | null>(null)

const selectedStationName = computed(() => stationMap[selectedStationKey.value] || '')

// 更新所有站點景點資訊
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

const showAlert = (message: string) => {
  customAlert.value = message
  setTimeout(() => {
    customAlert.value = null
  }, 3000)
}

const selectStation = (key: string) => {
  selectedStationKey.value = key
  const stationName = stationMap[key] || '未知'
  weatherData.value = `正在為 ${stationName} 站抓取天氣...`
  setTimeout(() => {
    weatherData.value = `目前 ${stationName} 站天氣：晴朗，25°C (模擬資料)`
  }, 500)
}

const getAttractions = (key: string): string => {
  return stationAttractions[key] || '無已知景點 (抓取資料中...)'
}

const openPopup = () => {
  showExplorePopup.value = true
}

const closePopup = () => {
  showExplorePopup.value = false
}

const handleExploreConfirmed = (key: string, role: 'sender' | 'receiver') => {
  const stationName = stationMap[key] || '未知站'
  console.log(`[Popup Confirmed] 已選擇站點: ${stationName} (Key: ${key}), 角色: ${role}。`)

  closePopup()

  const routeName = role === 'sender' ? 'SenderView' : 'ReceiverView'

  try {
    // 傳遞 station key 作為路由參數
    router.push({
      name: routeName,
      params: {
        station: key,
      },
    })
    console.log(`[Router Push Success] 已導航至路由: ${routeName} (Key: ${key})`)
  } catch (error: any) {
    console.error('[Router Error] 導航失敗，請檢查路由名稱或參數:', error)
    showAlert(`導航失敗：請檢查路由配置。錯誤: ${error.message}`)
  }

  const roleText = role === 'sender' ? '發送方' : '選擇方'
  showAlert(`已確認！即將前往 ${stationName} 站，扮演 ${roleText}。`)
}

const introContents = ref<string[]>([
  'STEP 1: 選擇捷運站\n選擇松山新店線(綠線)想探索的捷運站。',
  'STEP 2: 確認目的\n1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
  'STEP 3: 發送邀約 / 選擇邀約\n此部分將根據 邀約發送方 or 邀約選擇方 而有不同操作方式。',
  'STEP 4: 填寫滿意度\n完成邀約後，系統會引導您填寫本次體驗的滿意度，以便優化配對服務。',
  'STEP 5: 成功配對\n當雙方確認並完成所有步驟後，恭喜您！邀約成功，準備出發吧！',
])
</script>

<style scoped>
/* 滾動條樣式，保留左側步驟指南的滾動條 */
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

/* 自定義 Alert 動畫 */
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

/* 確保地鐵站點的文字不會換行，且能正確定位 */
.whitespace-nowrap {
  white-space: nowrap;
}
</style>
