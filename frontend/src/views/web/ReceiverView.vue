<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-gray-100 overflow-hidden font-sans">
    <!-- 左側：步驟指南 -->
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

    <!-- 右側: 邀約列表 -->
    <div class="flex flex-col w-full md:w-2/3 p-6 relative overflow-y-auto">
      <!-- 標題使用計算後的中文站名 -->
      <h1 class="text-2xl font-bold text-gray-800 border-b pb-3">探索{{ stationName }}站的邀約</h1>

      <!-- 加載中/錯誤提示 (模擬) -->
      <div v-if="isLoading" class="text-center py-10 text-gray-500">
        正在模擬載入 {{ stationName }} 站的邀約...
      </div>

      <!-- 邀約列表 -->
      <div v-else-if="invites.length > 0" class="space-y-4">
        <!-- 確保 InviteItem 的路徑和屬性正確 -->
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, watchEffect } from 'vue'
import MeetroIntroCard from '@/components/cards/MeetroIntroCard.vue'
import InviteItem from '@/components/items/InviteItem.vue'

// 站點英文 Key 到中文名稱的映射
const stationMap: Record<string, string> = {
  xindian: '新店',
  gongguan: '公館',
  nanjingFuxing: '南京復興',
  songshan: '松山',
}

// 1. **修正 Prop 名稱**：從 stationKey 改為 station
interface Props {
  station: string // 路由傳入的英文 Key
}
const props = defineProps<Props>()

// 計算屬性：將英文 Key 轉換為中文站名 (用於 UI 顯示)
const stationName = computed(() => stationMap[props.station] || '未知站')

// 邀約資料類型
interface Invite {
  id: number
  title: string
  senderName: string // 模擬發送者名稱
  date: string
  day: string
  location: string
  hasChat: boolean
}

// 狀態：管理邀約列表
const invites = ref<Invite[]>([])
const isLoading = ref(true)

/**
 * 模擬根據 stationKey 載入不同的邀約資料
 */
const loadInvites = (key: string) => {
  isLoading.value = true
  // 模擬異步載入
  setTimeout(() => {
    if (key === 'Gongguan') {
      invites.value = [
        {
          id: 1,
          title: '一起台大醉月湖散步',
          senderName: '周芳廷',
          date: '2025/11/12',
          day: '三',
          location: '水岸廣場',
          hasChat: true,
        },
        {
          id: 2,
          title: '水源市場小吃美食探索',
          senderName: 'Mr. 雪原',
          date: '2025/11/12',
          day: '三',
          location: '水源市場',
          hasChat: false,
        },
        {
          id: 3,
          title: '參觀自來水博物館',
          senderName: '王乙巴',
          date: '2025/11/13',
          day: '四',
          location: '自來水博物館',
          hasChat: false,
        },
      ]
    } else if (key === 'Songshan') {
      invites.value = [
        {
          id: 4,
          title: '饒河街夜市一起吃胡椒餅',
          senderName: '蔡雨思',
          date: '2025/11/14',
          day: '五',
          location: '饒河街夜市',
          hasChat: false,
        },
      ]
    } else {
      invites.value = []
    }
    isLoading.value = false
    console.log(`[Data Mock] 已載入 ${invites.value.length} 筆 ${stationName.value} 站的邀約。`)
  }, 500)
}

// 監聽 station 變化，並載入對應資料
watchEffect(() => {
  loadInvites(props.station)
})

// 處理 InviteItem 發出的事件
const handleViewDetails = (id: number) => {
  console.log(`[Action] 查看邀約 ID: ${id} 的詳細資訊`)
}

const handleAccept = (id: number) => {
  console.log(`[Action] 接受邀約 ID: ${id}`)
  // 實作接受邀約的邏輯 (可能更新狀態，並開啟聊天室)
  console.log(`[Action Status] 您已接受邀約 ID: ${id}，準備進入聊天室 (模擬成功)。`)
  // 模擬將此邀約從列表中移除或改變狀態
  invites.value = invites.value
    .map((i) => (i.id === id ? { ...i, hasChat: true } : i))
    .filter((i) => i.id !== id) // 模擬被移除，因為已經處理
}

const handleReject = (id: number) => {
  console.log(`[Action] 拒絕/刪除邀約 ID: ${id}`)
  // 實作刪除邀約的邏輯 (僅從本地列表移除)
  invites.value = invites.value.filter((i) => i.id !== id)
  console.log(`[Action Status] 邀約 ID: ${id} 已從列表中移除 (模擬拒絕/刪除)。`)
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
