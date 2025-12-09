<template>
  <div class="min-h-screen bg-[#FFF0F0] pb-20 relative font-sans">
    <div class="sticky top-0 z-10 bg-[#FFF0F0] pt-6 px-4">
      <div class="flex w-full max-w-6xl mx-auto bg-white shadow-sm rounded-2xl overflow-hidden">
        <div
          @click="activeTab = 0"
          class="flex-1 py-4 text-center cursor-pointer transition-all duration-300 relative font-bold tracking-wider text-lg"
          :class="
            activeTab === 0
              ? 'bg-[#E8F5E9] text-[#008659]'
              : 'bg-white text-gray-400 hover:bg-gray-50'
          "
        >
          初步接受邀約列表
          <div
            v-if="activeTab === 0"
            class="absolute bottom-0 left-0 right-0 h-1 bg-[#50C895]"
          ></div>
        </div>

        <div
          @click="activeTab = 1"
          class="flex-1 py-4 text-center cursor-pointer transition-all duration-300 relative font-bold tracking-wider text-lg"
          :class="
            activeTab === 1
              ? 'bg-[#E8F5E9] text-[#008659]'
              : 'bg-white text-gray-400 hover:bg-gray-50'
          "
        >
          完成赴約 ｜ 尚未填寫滿意度
          <div
            v-if="activeTab === 1"
            class="absolute bottom-0 left-0 right-0 h-1 bg-[#50C895]"
          ></div>
        </div>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-4 py-6 space-y-8">
      <div v-if="activeTab === 0" class="space-y-6 animate-fadeIn">
        <div
          v-if="pendingInvites.length === 0"
          class="text-center text-gray-500 py-16 bg-white/50 rounded-xl"
        >
          目前沒有初步接受的邀約，快去
          <router-link to="/" class="text-[#008659] font-bold underline hover:text-[#1b5e20]"
            >探索</router-link
          >
          吧！
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <InviteCard
            v-for="invite in pendingInvites"
            :key="invite.id"
            :invite="invite"
            type="pending"
            @view-details="handleViewDetails(invite)"
            @confirm="handleConfirmAppointment(invite.id)"
            @decline="handleDecline(invite.id)"
          />
        </div>
      </div>

      <div v-else class="space-y-6 animate-fadeIn">
        <div
          v-if="confirmedInvites.length === 0"
          class="text-center text-gray-500 py-16 bg-white/50 rounded-xl"
        >
          尚無待填寫滿意度的邀約。
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <InviteCard
            v-for="invite in confirmedInvites"
            :key="invite.id"
            :invite="invite"
            type="confirmed"
            @view-details="handleViewDetails(invite)"
            @feedback="openFeedbackModal(invite.id, invite.is_current_user_sender)"
          />
        </div>
      </div>
    </div>

    <InviteDetailPopup
      v-if="showDetailPopup && selectedInvite"
      :invite="selectedInviteForPopup"
      @close="showDetailPopup = false"
    />

    <FeedbackPopup
      v-if="showFeedbackModal"
      :match-id="selectedMatchId"
      @close="showFeedbackModal = false"
      @submitted="handleFeedbackSubmitted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import InviteCard, { type InviteHistoryItem } from '@/components/cards/InviteCard.vue' // 🚨 導入修正後的 InviteCard
import InviteDetailPopup from '@/components/web/PopupBox/InviteDetailPopup.vue'
import FeedbackPopup from '@/components/web/PopupBox/FeedbackPopup.vue'
import request from '@/utils/request'

// 🚨 修正：擴展 InviteHistoryItem 介面 (與後端 MatchItemResponse 匹配)
interface InviteHistoryItem {
  id: number
  partnerName: string
  partnerGender: string
  stationName: string
  location: string
  status: 'pending' | 'confirmed' | 'rejected' | string
  inviteDate: string | Date
  sender_rating: number | null
  receiver_rating: number | null
  is_current_user_sender: boolean // 🚨 來自後端
  googleMapLink?: string
}

const activeTab = ref(0)
const showDetailPopup = ref(false)
const selectedInvite = ref<InviteHistoryItem | null>(null)
const allInvites = ref<InviteHistoryItem[]>([])

const showFeedbackModal = ref(false)
const selectedMatchId = ref<number>(0)
const currentUserIsSender = ref(false)

// --- API: 獲取資料 ---
const fetchHistory = async () => {
  try {
    const res = await request.get('/api/matches/history')
    allInvites.value = res as any
  } catch (error) {
    console.error('獲取歷史紀錄失敗:', error)
  }
}

onMounted(() => {
  fetchHistory()
})

// --- Computed ---
const pendingInvites = computed(() => allInvites.value.filter((i) => i.status === 'pending'))

// 🚨 修正：過濾出狀態為 confirmed 且當前使用者尚未評分的 Match
const confirmedInvites = computed(() =>
  allInvites.value.filter((i) => {
    if (i.status !== 'confirmed') return false

    if (i.is_current_user_sender) {
      // Sender 檢查 sender_rating
      return i.sender_rating === null
    } else {
      // Receiver 檢查 receiver_rating
      return i.receiver_rating === null
    }
  }),
)

const selectedInviteForPopup = computed(() => {
  if (!selectedInvite.value) return {} as any

  const dateObj = new Date(selectedInvite.value.inviteDate)
  const dateStr = dateObj.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
  const dayMap = ['日', '一', '二', '三', '四', '五', '六']
  const dayStr = dayMap[dateObj.getDay()]

  return {
    id: selectedInvite.value.id,
    senderName: selectedInvite.value.partnerName,
    title: `與 ${selectedInvite.value.partnerName} 的邀約`,
    date: dateStr,
    day: dayStr,
    stationName: selectedInvite.value.stationName,
    location: selectedInvite.value.location,
    googleMapLink: selectedInvite.value.googleMapLink || '#',
  }
})

// --- Actions ---

const handleViewDetails = (invite: InviteHistoryItem) => {
  selectedInvite.value = invite
  showDetailPopup.value = true
}

const openFeedbackModal = (id: number, isSender: boolean) => {
  selectedMatchId.value = id
  currentUserIsSender.value = isSender
  showFeedbackModal.value = true
}

const handleConfirmAppointment = async (id: number) => {
  const target = allInvites.value.find((i) => i.id === id)
  if (target) {
    if (confirm(`確定要赴約 ${target.partnerName} 的邀約嗎？`)) {
      try {
        await request.patch(`/api/matches/${id}/status`, { status: 'confirmed' })

        target.status = 'confirmed'
        activeTab.value = 1
      } catch (error) {
        alert('更新失敗')
      }
    }
  }
}

const handleDecline = async (id: number) => {
  if (confirm('確定要婉拒這個邀約嗎？此動作無法復原。')) {
    try {
      await request.patch(`/api/matches/${id}/status`, { status: 'rejected' })

      allInvites.value = allInvites.value.filter((i) => i.id !== id)
    } catch (error) {
      alert('更新失敗')
    }
  }
}

// 處理滿意度提交後的事件
const handleFeedbackSubmitted = ({ matchId, rating }: { matchId: number; rating: number }) => {
  const target = allInvites.value.find((i) => i.id === matchId)
  if (target) {
    // 根據提交時的角色來更新正確的評分欄位
    if (target.is_current_user_sender) {
      target.sender_rating = rating
    } else {
      target.receiver_rating = rating
    }
  }
  // 重新載入列表，讓已評分的項目從列表中消失
  fetchHistory()
}
</script>

<style scoped>
/* Style 保持不變 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.4s ease-out forwards;
}
</style>
