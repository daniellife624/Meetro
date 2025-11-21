<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-gray-100 overflow-hidden font-sans">
    <div
      class="w-full md:w-1/3 bg-white border-r border-gray-200 p-6 flex flex-col overflow-y-auto max-h-full md:max-h-screen"
    >
      <h1 class="text-2xl font-extrabold mb-4 text-gray-800 border-b-2 border-[#E8F5E9] pb-3">
        Meetro 選擇方步驟指南
      </h1>
      <div class="intro-cards-scroll-area flex-grow overflow-y-auto pr-3">
        <div class="space-y-6">
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

    <div class="flex flex-col w-full md:w-2/3 pl-6 py-8 pr-0 relative overflow-y-auto">
      <div class="flex items-center gap-4 mb-8 pr-6 border-b border-gray-200 pb-4">
        <div
          class="flex flex-col items-center justify-center bg-[#286047] text-white w-20 h-20 rounded-2xl shadow-lg flex-shrink-0"
        >
          <span class="text-xs opacity-80 font-medium tracking-widest">MRT</span>
          <span class="text-2xl font-bold tracking-widest">{{ stationName.slice(0, 2) }}</span>
        </div>

        <div class="flex flex-col">
          <h1 class="text-3xl font-extrabold text-gray-800 tracking-wide flex items-center gap-2">
            探索邀約
          </h1>
          <p class="text-gray-500 text-sm mt-1 font-medium">
            目前正在瀏覽
            <span class="text-[#286047] font-bold text-base mx-1">{{ stationName }}</span>
            周邊的活動
          </p>
        </div>
      </div>

      <div
        v-if="isLoading"
        class="text-center py-20 text-gray-500 flex flex-col items-center gap-3"
      >
        <div
          class="w-8 h-8 border-4 border-[#286047] border-t-transparent rounded-full animate-spin"
        ></div>
        <p>正在搜尋 {{ stationName }} 站的邀約...</p>
      </div>

      <div v-else-if="invites.length > 0" class="space-y-5 pr-0">
        <InviteItem
          v-for="invite in invites"
          :key="invite.id"
          :invite="invite"
          @view-details="handleViewDetails"
          @accept="handleAccept"
          @reject="handleReject"
        />
      </div>

      <div v-else class="flex flex-col items-center justify-center py-20 text-gray-400 pr-6">
        <SvgItem name="search" size="16" class="mb-4 text-gray-300" />
        <p class="text-lg font-medium">目前 {{ stationName }} 站沒有公開的邀約...</p>
        <p class="text-sm">試試看切換到其他站點吧！</p>
      </div>
    </div>

    <InviteDetailPopup
      v-if="showDetailPopup && selectedInvite"
      :invite="selectedInvite"
      @close="closeDetailPopup"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, watchEffect, h, type Component } from 'vue'
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'
import InviteItem from '@/components/items/InviteItem.vue'
import InviteDetailPopup from '@/components/web/PopupBox/InviteDetailPopup.vue'
import SvgItem from '@/components/icons/SvgItem.vue'

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
interface Props {
  stationKey: string
}
const props = defineProps<Props>()
const stationName = computed(() => {
  const key = props.stationKey?.toLowerCase().trim() || ''
  return stationMap[key] || '未知'
})
interface Invite {
  id: number
  title: string
  senderName: string
  date: string
  day: string
  location: string
  hasChat: boolean
  stationName: string
  googleMapLink: string
}
const invites = ref<Invite[]>([])
const isLoading = ref(true)
const showDetailPopup = ref(false)
const selectedInvite = ref<Invite | null>(null)

const loadInvites = (key: string) => {
  isLoading.value = true
  const normalizedKey = key.toLowerCase().trim()
  setTimeout(() => {
    if (normalizedKey === 'gongguan') {
      invites.value = [
        {
          id: 1,
          title: '下課沒事想去河岸邊走走',
          senderName: '周彥廷',
          date: '2025/11/12',
          day: '三',
          location: '公館水岸廣場',
          hasChat: true,
          stationName: '公館站',
          googleMapLink: '#',
        },
        {
          id: 2,
          title: '水源市場小吃美食探索',
          senderName: 'Mr. 雪原',
          date: '2025/11/12',
          day: '三',
          location: '水源市場',
          hasChat: false,
          stationName: '公館站',
          googleMapLink: '#',
        },
        {
          id: 3,
          title: '參觀自來水博物館',
          senderName: '王乙巴',
          date: '2025/11/13',
          day: '四',
          location: '自來水博物館',
          hasChat: false,
          stationName: '公館站',
          googleMapLink: '#',
        },
      ]
    } else if (normalizedKey === 'songshan') {
      invites.value = [
        {
          id: 4,
          title: '饒河街夜市一起吃胡椒餅',
          senderName: '蔡雨思',
          date: '2025/11/14',
          day: '五',
          location: '饒河街夜市',
          hasChat: false,
          stationName: '松山站',
          googleMapLink: '#',
        },
      ]
    } else {
      invites.value = []
    }
    isLoading.value = false
  }, 500)
}
watchEffect(() => {
  loadInvites(props.stationKey)
})
const handleViewDetails = (id: number) => {
  const target = invites.value.find((i) => i.id === id)
  if (target) {
    selectedInvite.value = target
    showDetailPopup.value = true
  }
}
const closeDetailPopup = () => {
  showDetailPopup.value = false
  setTimeout(() => {
    selectedInvite.value = null
  }, 200)
}
const handleAccept = (id: number) => {
  console.log('Accept', id)
}
const handleReject = (id: number) => {
  invites.value = invites.value.filter((i) => i.id !== id)
}

// Icons & Steps
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

const introSteps = ref([
  { title: '選擇捷運站', description: '選擇松山新店線(綠線)想探索的捷運站。', icon: MapPinIcon },
  {
    title: '確認目的',
    description: '1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
    icon: TargetIcon,
  },
  {
    title: '選擇邀約',
    description:
      '點選該捷運站後，即會跳出於此捷運站發送邀約的發送方。你可以與有興趣邀邀約的發送方聊天，決定是否赴約。',
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
</style>
