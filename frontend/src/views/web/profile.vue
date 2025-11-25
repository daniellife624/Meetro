<template>
  <div class="min-h-screen bg-[#FFF0F0] px-4 font-sans flex flex-col">
    <div class="container mx-auto flex-grow flex items-start justify-center pt-20">
      <ProfileCard :user="userData" @change-password="showPasswordPopup = true" />
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
// Script 保持不變
import { ref } from 'vue'
import ProfileCard, { type UserProfile } from '@/components/cards/ProfileCard.vue'
import PopupBoxLayout from '@/components/web/PopupBox/PopupBoxLayout.vue'
import ChangePasswordPopup from '@/components/web/PopupBox/ChangePasswordPopup.vue'

const userData = ref<UserProfile>({
  name: '王小明',
  birthday: '2002-08-15',
  gender: '男性',
  email: 'wang.min@gmail.com',
  simulationCount: 5,
  successRate: 85,
})

const showPasswordPopup = ref(false)

const handleChangePasswordSubmit = (data: any) => {
  console.log('修改密碼資料:', data)
  // 這裡呼叫 API
  alert('密碼修改成功！')
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
