<template>
  <div class="min-h-screen bg-gray-50 pb-20 relative">
    <div class="flex w-full bg-white shadow-sm sticky top-0 z-10">
      <div
        @click="activeTab = 0"
        class="flex-1 py-4 text-center cursor-pointer transition-colors duration-300 relative"
        :class="
          activeTab === 0
            ? 'bg-[#81c784] text-white'
            : 'bg-[#ffebee] text-gray-600 hover:bg-gray-100'
        "
      >
        <span class="font-bold tracking-wide">初步接受邀約列表</span>
        <div v-if="activeTab === 0" class="absolute right-0 top-0 bottom-0 w-1 bg-[#286047]"></div>
      </div>

      <div
        @click="activeTab = 1"
        class="flex-1 py-4 text-center cursor-pointer transition-colors duration-300"
        :class="
          activeTab === 1
            ? 'bg-[#81c784] text-white'
            : 'bg-[#ffebee] text-gray-600 hover:bg-gray-100'
        "
      >
        <span class="font-bold tracking-wide">完成赴約 ｜ 尚未填寫滿意度</span>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <div v-if="activeTab === 0" class="space-y-6">
        <div v-if="pendingInvites.length === 0" class="text-center text-gray-500 py-10">
          目前沒有初步接受的邀約，快去
          <router-link to="/" class="text-[#286047] font-bold underline">探索</router-link> 吧！
        </div>

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

      <div v-else class="space-y-6">
        <div v-if="confirmedInvites.length === 0" class="text-center text-gray-500 py-10">
          尚無待填寫滿意度的邀約。
        </div>

        <InviteCard
          v-for="invite in confirmedInvites"
          :key="invite.id"
          :invite="invite"
          type="confirmed"
          @view-details="handleViewDetails(invite)"
          @feedback="handleFeedback(invite.id)"
        />
      </div>
    </div>

    <div class="fixed bottom-6 right-6 z-30">
      <button
        @click="openChatRoom"
        class="flex items-center justify-center px-6 py-3 bg-[#FF8A80] text-white font-bold rounded-l-full rounded-t-full shadow-lg hover:bg-[#ff5252] transition-transform hover:scale-105"
      >
        <span class="mr-2">💬</span> 聊天室
      </button>
    </div>

    <footer
      class="w-full bg-gray-700 text-white text-center py-4 text-xs fixed bottom-0 left-0 z-20"
    >
      © 2025 MeetTro 相遇地圖 版權所有
    </footer>

    <InviteDetailPopup
      v-if="showDetailPopup && selectedInvite"
      :invite="selectedInviteForPopup"
      @close="showDetailPopup = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import InviteCard, { type InviteHistoryItem } from '@/components/cards/InviteCard.vue'
import InviteDetailPopup from '@/components/web/PopupBox/InviteDetailPopup.vue'
// 確保路徑正確

const activeTab = ref(0)
const showDetailPopup = ref(false)
const selectedInvite = ref<InviteHistoryItem | null>(null)

// --- 模擬資料 (Mock Data) ---
// 實際上這些資料應該來自 API 或 Pinia Store
const allInvites = ref<InviteHistoryItem[]>([
  {
    id: 101,
    senderName: '王小明',
    senderGender: '男性',
    senderAvatar: 'https://randomuser.me/api/portraits/men/32.jpg',
    stationName: '公館站',
    location: '公館水岸廣場',
    status: 'pending', // 狀態：初步接受
  },
  {
    id: 102,
    senderName: '陳美麗',
    senderGender: '女性',
    senderAvatar: 'https://randomuser.me/api/portraits/women/44.jpg',
    stationName: '中山站',
    location: '光點台北電影院',
    status: 'confirmed', // 狀態：已赴約 (會在 Tab 2)
  },
  {
    id: 103,
    senderName: '林大衛',
    senderGender: '男性',
    senderAvatar: 'https://randomuser.me/api/portraits/men/85.jpg',
    stationName: '新店站',
    location: '碧潭吊橋',
    status: 'pending',
  },
])

// --- Computed: 自動分類 ---
const pendingInvites = computed(() => allInvites.value.filter((i) => i.status === 'pending'))

const confirmedInvites = computed(() => allInvites.value.filter((i) => i.status === 'confirmed'))

// 為了配合 InviteDetailPopup 的資料結構轉換 (如果欄位名稱不完全一樣的話)
const selectedInviteForPopup = computed(() => {
  if (!selectedInvite.value) return {} as any
  return {
    id: selectedInvite.value.id,
    senderName: selectedInvite.value.senderName,
    title: `與 ${selectedInvite.value.senderName} 的邀約`, // 模擬標題
    date: '2025-11-20', // 模擬日期
    day: '六',
    stationName: selectedInvite.value.stationName,
    location: selectedInvite.value.location,
    googleMapLink: '#', // 模擬連結
  }
})

// --- Actions ---

// 1. 查看細節
const handleViewDetails = (invite: InviteHistoryItem) => {
  selectedInvite.value = invite
  showDetailPopup.value = true
}

// 2. 確定赴約 (關鍵邏輯：Pending -> Confirmed)
const handleConfirmAppointment = (id: number) => {
  const target = allInvites.value.find((i) => i.id === id)
  if (target) {
    if (
      confirm(`確定要赴約 ${target.senderName} 的邀約嗎？\n這將會把此卡片移動到「完成赴約」列表。`)
    ) {
      // 修改狀態，Vue 的 reactivity 會自動把它搬到 Tab 2
      target.status = 'confirmed'
      // 自動切換到 Tab 2 讓使用者看到結果
      activeTab.value = 1
    }
  }
}

// 3. 決定婉拒 (從列表中移除)
const handleDecline = (id: number) => {
  if (confirm('確定要婉拒這個邀約嗎？此動作無法復原。')) {
    allInvites.value = allInvites.value.filter((i) => i.id !== id)
  }
}

// 4. 填寫滿意度
const handleFeedback = (id: number) => {
  alert('即將開啟滿意度填寫表單 (待開發功能)')
  // 這裡未來可以導航到 feedback 頁面或開啟 Modal
}

// 5. 開啟聊天室
const openChatRoom = () => {
  // 這裡未來可以開啟 Chat Modal 或導航
  console.log('Open Chat Room')
}
</script>

<style scoped>
/* 隱藏捲軸但保留滾動功能 (可選) */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
