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
            :content="step.content"
            :icon-name="step.icon"
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
import { ref, computed, defineProps, watchEffect } from 'vue'
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'
import InviteItem from '@/components/items/InviteItem.vue'
import InviteDetailPopup from '@/components/web/PopupBox/InviteDetailPopup.vue'
import SvgItem from '@/components/icons/SvgItem.vue'
import request from '@/utils/request'

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

const loadInvites = async (key: string) => {
  isLoading.value = true
  invites.value = [] // 清空舊資料

  const normalizedKey = key.toLowerCase().trim()

  try {
    // 呼叫後端 API: GET /api/invites?station_key=xxx
    const res: any = await request.get('/api/invites', {
      params: { station_key: normalizedKey },
    })

    if (res && Array.isArray(res)) {
      invites.value = res.map((item: any) => {
        const d = new Date(item.meet_time)
        // 簡單的日期格式化
        const dayMap = ['日', '一', '二', '三', '四', '五', '六']
        const dateStr = `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`

        return {
          id: item.id,
          title: item.title,
          senderName: item.sender ? item.sender.name : '未知用戶',
          date: dateStr,
          day: dayMap[d.getDay()],
          location: item.location_name,
          hasChat: false,
          stationName: stationName.value,
          googleMapLink: `http://googleusercontent.com/maps.google.com/?q=${item.latitude},${item.longitude}`,
        }
      })
    }
  } catch (error) {
    console.error('載入邀約失敗:', error)
  } finally {
    isLoading.value = false
  }
}

watchEffect(() => {
  if (props.stationKey) {
    loadInvites(props.stationKey)
  }
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

const handleAccept = async (id: number) => {
  try {
    // 呼叫後端接受 API
    await request.post(`/api/matches/${id}/accept`)
    alert('成功接受邀約！請至「邀約歷史」查看。')

    // 從列表中移除該邀約
    invites.value = invites.value.filter((i) => i.id !== id)
  } catch (error: any) {
    const msg = error.response?.data?.detail || '接受失敗'
    alert(msg)
  }
}

const handleReject = (id: number) => {
  // 前端暫時移除顯示 (不呼叫後端 API，除非有拒絕 API)
  invites.value = invites.value.filter((i) => i.id !== id)
}

const introSteps = [
  { title: '選擇捷運站', content: '選擇松山新店線(綠線)想探索的捷運站。', icon: 'location-dot' },
  {
    title: '確認目的',
    content: '1. 想找人一起參與 (發送方)\n2. 尋找有趣活動 (選擇方)',
    icon: 'target',
  },
  {
    title: '選擇邀約',
    content: '點選該捷運站後，即會跳出於此捷運站發送邀約的發送方...',
    icon: 'send',
  },
  {
    title: '填寫滿意度',
    content: '完成邀約後，系統會引導您填寫本次體驗的滿意度...',
    icon: 'check',
  },
  {
    title: '模擬成功機率',
    content: '當雙方完成滿意度填寫後，即可於個人帳戶檢視模擬下一次成功機率之結果',
    icon: 'party',
  },
]
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
