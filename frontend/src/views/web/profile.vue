<template>
  <div class="min-h-screen bg-[#FFF0F0] px-4 font-sans flex flex-col">
    <div class="container mx-auto flex-grow flex items-start justify-center pt-20">
      <ProfileCard
        v-if="userData.email"
        :user="userData"
        @change-password="showPasswordPopup = true"
      />
      <div v-else class="text-center text-gray-500 mt-20">資料載入中...</div>
    </div>

    <PopupBoxLayout
      v-if="showPasswordPopup"
      title="修改密碼"
      :cancel-callback="() => (showPasswordPopup = false)"
      :use-form="false"
    >
      <ChangePasswordPopup
        @cancel="showPasswordPopup = false"
        @submit="handleChangePasswordSubmit"
      />
    </PopupBoxLayout>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ProfileCard, { type UserProfile } from '@/components/cards/ProfileCard.vue'
import PopupBoxLayout from '@/components/web/PopupBox/PopupBoxLayout.vue'
import ChangePasswordPopup from '@/components/web/PopupBox/ChangePasswordPopup.vue'
import request from '@/utils/request'

interface UserProfile {
  name: string
  birthday: string
  gender: string
  email: string
  simulationCount: number
  successRate: number
  weatherScore?: number
  placeScore?: number
  historyScore?: number
}
// 初始化為空物件，等待 API 填入
const userData = ref<UserProfile>({
  name: '',
  birthday: '',
  gender: '',
  email: '',
  simulationCount: 0,
  successRate: 0,
})

const showPasswordPopup = ref(false)

const fetchUserProfile = async () => {
  try {
    const userRes: any = await request.get('/auth/me')
    const stationKey = 'gongguan'
    const testLat = 25.013
    const testLng = 121.537

    const rateRes: any = await request.get('/api/success/estimate', {
      params: {
        station_key: stationKey,
        lat: testLat,
        lng: testLng,
      },
    })

    console.log('成功率估算結果:', rateRes)

    // 計算模擬次數
    let count = 0
    if (rateRes.history_label && rateRes.history_label.startsWith('有 ')) {
      const match = rateRes.history_label.match(/有 (\d+) 筆紀錄/)
      if (match) {
        count = parseInt(match[1], 10)
      }
    }

    // 將後端資料映射到前端介面
    userData.value = {
      name: userRes.name, // 對應 UserOut 的 name
      email: userRes.email, // 對應 UserOut 的 email
      gender: userRes.gender || '未設定',
      birthday: userRes.birthday || '未設定',
      simulationCount: count,
      successRate: rateRes.success_rate || 0,
    }
  } catch (error) {
    console.error('獲取個人資料或成功率失敗:', error)
    alert('無法取得使用者資料或模擬成功率，請檢查後端服務')
  }
}

// 畫面載入時執行
onMounted(() => {
  fetchUserProfile()
})

const handleChangePasswordSubmit = (data: any) => {
  console.log('修改密碼資料:', data)
  // TODO: 這裡未來可以串接修改密碼 API
  alert('密碼修改成功！(模擬)')
  showPasswordPopup.value = false
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
.container {
  animation: fadeIn 0.5s ease-out forwards;
}
</style>
