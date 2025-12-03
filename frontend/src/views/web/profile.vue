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

// 初始化為空物件，等待 API 填入
const userData = ref<UserProfile>({
  name: '',
  birthday: '',
  gender: '',
  email: '',
  simulationCount: 0, // 目前後端尚未實作此欄位，先給預設值
  successRate: 0, // 目前後端尚未實作此欄位，先給預設值
})

const showPasswordPopup = ref(false)

const fetchUserProfile = async () => {
  try {
    // 呼叫 /auth/me (request.ts 的攔截器會自動帶上 Token)
    const res: any = await request.get('/auth/me')

    console.log('使用者資料:', res)

    // 將後端資料映射到前端介面
    userData.value = {
      name: res.name, // 對應 UserOut 的 name
      email: res.email, // 對應 UserOut 的 email
      gender: res.gender || '未設定',
      birthday: res.birthday || '未設定',
      simulationCount: 5, // 暫時寫死 (模擬數據)
      successRate: 85, // 暫時寫死 (模擬數據)
    }
  } catch (error) {
    console.error('獲取個人資料失敗:', error)
    alert('無法取得使用者資料，請重新登入')
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
