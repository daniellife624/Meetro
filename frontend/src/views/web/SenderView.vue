<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-[#f1f8e9] overflow-hidden font-sans">
    <div
      class="w-full md:w-1/3 bg-white border-r border-gray-200 p-6 flex flex-col overflow-y-auto max-h-full md:max-h-screen"
    >
      <h1 class="text-2xl font-extrabold mb-4 text-[#008659] border-b-2 border-[#E8F5E9] pb-3">
        Meetro 發送方步驟指南
      </h1>
      <div class="intro-cards-scroll-area flex-grow overflow-y-auto pr-3">
        <div class="space-y-4">
          <MeetroIntroCard
            v-for="(step, index) in introSteps"
            :key="index"
            :step-number="index + 1"
            :title="step.title"
            :content="step.description"
            :icon="step.icon"
          />
        </div>
      </div>
    </div>

    <div class="flex flex-col w-full md:w-2/3 p-6 relative overflow-y-auto bg-white h-full">
      <h2 class="text-3xl font-extrabold text-[#008659] mb-6 border-b pb-3">
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
            placeholder="請簡述您的邀約內容..."
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#008659] resize-none"
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
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#008659]"
          />
        </div>

        <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg shadow-sm">
          <label class="block text-lg font-semibold text-[#1b5e20] mb-2"> 【地】邀約地點 </label>
          <input
            id="autocomplete-input"
            type="text"
            v-model="invitation.locationName"
            placeholder="請輸入或在地圖上點擊來選擇地點"
            class="w-full p-3 mb-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#008659]"
          />
          <div id="map" class="w-full h-96 rounded-lg shadow-md border-2 border-[#008659]"></div>
          <p class="text-sm text-gray-600 mt-2">
            選定座標：<span class="font-mono text-xs text-red-600">{{ invitation.latLng }}</span>
          </p>
        </div>
      </div>

      <div class="flex justify-end items-center pt-6 border-t border-gray-200 mt-6">
        <button
          @click="sendInvitation"
          :disabled="!isFormValid"
          class="bg-[#008659] text-white font-bold px-12 py-3 rounded-full hover:bg-green-700 disabled:bg-gray-400 shadow-xl"
        >
          發送邀約
        </button>
      </div>
    </div>

    <div
      v-if="showSuccessModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-filter backdrop-blur-sm"
    >
      <div class="bg-white rounded-2xl p-8 max-w-sm w-full mx-4 shadow-2xl text-center">
        <div
          class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4"
        >
          <svg class="w-8 h-8 text-[#008659]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
            class="w-full py-3 bg-[#008659] text-white font-bold rounded-xl hover:bg-green-800"
          >
            回到首頁
          </button>
          <button
            @click="showSuccessModal = false"
            class="w-full py-3 text-gray-500 font-bold rounded-xl hover:bg-gray-100"
          >
            繼續留在本頁
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, onMounted, h, type Component } from 'vue'
import { useRouter } from 'vue-router'
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'

const router = useRouter()

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
  return stationMap[key] || '未知'
})
const invitation = ref({
  title: '',
  time: '',
  locationName: '',
  latLng: '',
  stationKey: props.stationKey,
})
const showSuccessModal = ref(false)

// 【修正重點 1】定義 Icon 並更新資料結構 (introSteps)
// 這裡的 Icon 定義與 index.vue 相同，保持風格一致
const MapPinIcon = h(
  'svg',
  {
    xmlns: 'http://www.w3.org/2000/svg',
    width: '24',
    height: '24',
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': '2',
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
  },
  [
    h('path', { d: 'M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z' }),
    h('circle', { cx: '12', cy: '10', r: '3' }),
  ],
)
const TargetIcon = h(
  'svg',
  {
    xmlns: 'http://www.w3.org/2000/svg',
    width: '24',
    height: '24',
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': '2',
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
  },
  [
    h('circle', { cx: '12', cy: '12', r: '10' }),
    h('circle', { cx: '12', cy: '12', r: '6' }),
    h('circle', { cx: '12', cy: '12', r: '2' }),
  ],
)
const SendIcon = h(
  'svg',
  {
    xmlns: 'http://www.w3.org/2000/svg',
    width: '24',
    height: '24',
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': '2',
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
  },
  [h('path', { d: 'm22 2-7 20-4-9-9-4Z' }), h('path', { d: 'M22 2 11 13' })],
)
const CheckCircleIcon = h(
  'svg',
  {
    xmlns: 'http://www.w3.org/2000/svg',
    width: '24',
    height: '24',
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': '2',
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
  },
  [
    h('path', { d: 'M22 11.08V12a10 10 0 1 1-5.93-9.14' }),
    h('polyline', { points: '22 4 12 14.01 9 11.01' }),
  ],
)
const PartyPopperIcon = h(
  'svg',
  {
    xmlns: 'http://www.w3.org/2000/svg',
    width: '24',
    height: '24',
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': '2',
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
  },
  [
    h('path', {
      d: 'M5.8 11.3 2 12l.7-3.8L2 4.4 5.8 5l.7-3.8 3.8.7.7-3.8 3.8.7.7-3.8 3.8.7 3.8-3.8',
    }),
    h('path', { d: 'M4 22h16' }),
    h('path', { d: 'M10 22v-4a2 2 0 1 1 4 0v4' }),
    h('path', { d: 'm14 14.5-2.5 2.5' }),
    h('path', { d: 'm10 14.5 2.5 2.5' }),
    h('path', { d: 'm9 13.5 1 1' }),
    h('path', { d: 'm15 13.5-1 1' }),
    h('path', { d: 'm12 11.5 0 1' }),
  ],
)

interface IntroStep {
  title: string
  description: string
  icon: Component
}

// 重新定義資料結構
const introSteps = ref<IntroStep[]>([
  {
    title: '選擇捷運站',
    description: '選擇松山新店線(綠線)想探索的捷運站。',
    icon: MapPinIcon,
  },
  {
    title: '確認目的',
    description: '1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
    icon: TargetIcon,
  },
  {
    title: '發送方發送邀約',
    description:
      '點選該捷運站後，即會跳出輸入欄位完成邀約目的（事）、邀約時間（時）、邀約地點（地），即可立即發送邀約',
    icon: SendIcon,
  },
  {
    title: '填寫滿意度',
    description: '完成邀約後，系統會引導您填寫本次體驗的滿意度，以便優化配對服務。',
    icon: CheckCircleIcon,
  },
  {
    title: '成功配對',
    description: '當雙方確認並完成所有步驟後，恭喜您！邀約成功，準備出發吧！',
    icon: PartyPopperIcon,
  },
])

// ... (保留 isFormValid, initMap, sendInvitation, goHome, onMounted 等邏輯) ...
const isFormValid = computed(
  () =>
    invitation.value.title.trim() !== '' &&
    invitation.value.time !== '' &&
    invitation.value.latLng !== '',
)
const initMap = () => {
  /* ...保留原程式碼... */
}
const sendInvitation = () => {
  /* ...保留原程式碼... */
}
const goHome = () => {
  router.push({ name: 'home' })
}
;(window as any).initMap = initMap
onMounted(() => {
  /* ...保留原程式碼... */
})
</script>

<style scoped>
/* ...保留原樣式... */
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
