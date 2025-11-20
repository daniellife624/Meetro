<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-gray-100 overflow-hidden font-sans">
    <div
      class="w-full md:w-1/3 bg-white border-r border-gray-200 p-6 flex flex-col overflow-y-auto max-h-full md:max-h-screen"
    >
      <h1 class="text-2xl font-extrabold mb-4 text-[#E3002C] border-b-2 border-[#E8F5E9] pb-3">
        Meetro 選擇方步驟指南
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

    <div class="flex flex-col w-full md:w-2/3 pl-6 py-6 pr-0 relative overflow-y-auto">
      <h1 class="text-2xl font-bold text-gray-800 border-b pb-3 pr-6">
        探索{{ stationName }}站的邀約
      </h1>

      <div v-if="isLoading" class="text-center py-10 text-gray-500">
        正在模擬載入 {{ stationName }} 站的邀約...
      </div>

      <div v-else-if="invites.length > 0" class="space-y-4">
        <InviteItem
          v-for="invite in invites"
          :key="invite.id"
          :invite="invite"
          @view-details="handleViewDetails"
          @accept="handleAccept"
          @reject="handleReject"
        />
      </div>

      <div v-else class="text-center py-10 text-gray-500">
        目前{{ stationName }}站沒有公開的邀約...
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
import { ref, computed, defineProps, watchEffect } from 'vue'
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'
import InviteItem from '@/components/items/InviteItem.vue'
import InviteDetailPopup from '@/components/web/PopupBox/InviteDetailPopup.vue'

const stationMap: Record<string, string> = {
  xindian: '新店',
  gongguan: '公館',
  nanjingfuxing: '南京復興',
  songshan: '松山',
}

interface Props {
  stationKey: string
}
const props = defineProps<Props>()

const stationName = computed(() => {
  const key = props.stationKey?.toLowerCase().trim() || ''
  return stationMap[key] || '未知'
})

// 【修改】擴充資料介面，加入 Popup 需要的資訊
interface Invite {
  id: number
  title: string
  senderName: string
  date: string
  day: string
  location: string
  hasChat: boolean
  stationName: string // 新增: 用於顯示站名
  googleMapLink: string // 新增: Google Map 連結
}

const invites = ref<Invite[]>([])
const isLoading = ref(true)

// 【新增】Popup 狀態控制
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
          title: '下課沒事想去河岸邊走走，有人要加一嗎', // 修改標題以符合截圖
          senderName: '周彥廷',
          date: '2025/11/12',
          day: '三',
          location: '公館水岸廣場',
          hasChat: true,
          stationName: '公館站',
          googleMapLink:
            'https://www.google.com/maps/place/%E5%85%AC%E9%A4%A8%E6%B0%B4%E5%B2%B8%E5%BB%A3%E5%A0%B4/@25.0112512,121.5284012,17z',
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
          googleMapLink: 'https://maps.google.com/?q=水源市場',
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
          googleMapLink: 'https://maps.google.com/?q=自來水博物館',
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
          googleMapLink: 'https://maps.google.com/?q=饒河街夜市',
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

// 【修改】點擊「詳細資訊」時的邏輯
const handleViewDetails = (id: number) => {
  // 找到對應的邀約資料
  const targetInvite = invites.value.find((i) => i.id === id)
  if (targetInvite) {
    selectedInvite.value = targetInvite
    showDetailPopup.value = true
    console.log(`[Action] 開啟詳細資訊: ${targetInvite.title}`)
  }
}

// 【新增】關閉 Popup
const closeDetailPopup = () => {
  showDetailPopup.value = false
  // 延遲清除資料避免動畫時內容突然消失 (可選)
  setTimeout(() => {
    selectedInvite.value = null
  }, 200)
}

const handleAccept = (id: number) => {
  // ... (維持原樣)
  console.log(`[Action] 接受邀約 ID: ${id}`)
}

const handleReject = (id: number) => {
  // ... (維持原樣)
  invites.value = invites.value.filter((i) => i.id !== id)
}

const introContents = ref<string[]>([
  'STEP 1: 選擇捷運站\n選擇松山新店線(綠線)想探索的捷運站。',
  'STEP 2: 確認目的\n1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
  'STEP 3: 選擇方選擇有興趣邀約\n點選該捷運站後，即會跳出於此捷運站發送邀約的發送方。你可以與有興趣邀邀約的發送方聊天，決定是否赴約。',
  'STEP 4: 填寫滿意度\n完成邀約後，系統會引導您填寫本次體驗的滿意度，以便優化配對服務。',
  'STEP 5: 成功配對\n當雙方確認並完成所有步驟後，恭喜您！邀約成功，準備出發吧！',
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
