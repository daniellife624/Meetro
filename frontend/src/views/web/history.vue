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
            @feedback="handleFeedback(invite.id)"
          />
        </div>
      </div>
    </div>

    <InviteDetailPopup
      v-if="showDetailPopup && selectedInvite"
      :invite="selectedInviteForPopup"
      @close="showDetailPopup = false"
    />
  </div>
</template>

<script setup lang="ts">
// Script 部分完全不需要修改，保持原樣即可
import { ref, computed } from 'vue'
import InviteCard, { type InviteHistoryItem } from '@/components/cards/InviteCard.vue'
import InviteDetailPopup from '@/components/web/PopupBox/InviteDetailPopup.vue'

const activeTab = ref(0)
const showDetailPopup = ref(false)
const selectedInvite = ref<InviteHistoryItem | null>(null)

const allInvites = ref<InviteHistoryItem[]>([
  {
    id: 101,
    senderName: '王小明',
    senderGender: '男性',
    stationName: '公館站',
    location: '公館水岸廣場',
    status: 'pending',
  },
  {
    id: 102,
    senderName: '陳美麗',
    senderGender: '女性',
    stationName: '中山站',
    location: '光點台北電影院',
    status: 'confirmed',
  },
  {
    id: 103,
    senderName: '林大衛',
    senderGender: '男性',
    stationName: '新店站',
    location: '碧潭吊橋',
    status: 'pending',
  },
])

const pendingInvites = computed(() => allInvites.value.filter((i) => i.status === 'pending'))
const confirmedInvites = computed(() => allInvites.value.filter((i) => i.status === 'confirmed'))

const selectedInviteForPopup = computed(() => {
  if (!selectedInvite.value) return {} as any
  return {
    id: selectedInvite.value.id,
    senderName: selectedInvite.value.senderName,
    title: `與 ${selectedInvite.value.senderName} 的邀約`,
    date: '2025-11-20',
    day: '六',
    stationName: selectedInvite.value.stationName,
    location: selectedInvite.value.location,
    googleMapLink: '#',
  }
})

const handleViewDetails = (invite: InviteHistoryItem) => {
  selectedInvite.value = invite
  showDetailPopup.value = true
}

const handleConfirmAppointment = (id: number) => {
  const target = allInvites.value.find((i) => i.id === id)
  if (target) {
    if (confirm(`確定要赴約 ${target.senderName} 的邀約嗎？`)) {
      target.status = 'confirmed'
      activeTab.value = 1
    }
  }
}

const handleDecline = (id: number) => {
  if (confirm('確定要婉拒這個邀約嗎？此動作無法復原。')) {
    allInvites.value = allInvites.value.filter((i) => i.id !== id)
  }
}

const handleFeedback = (id: number) => {
  alert('即將開啟滿意度填寫表單 (待開發功能)')
}

const openChatRoom = () => {
  console.log('Open Chat Room')
}
</script>

<style scoped>
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
