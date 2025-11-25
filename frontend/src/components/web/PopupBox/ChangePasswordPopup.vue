<template>
  <div class="text-left space-y-5">
    <div class="space-y-1">
      <label class="text-sm font-bold text-gray-700">舊密碼</label>
      <input
        v-model="form.oldPassword"
        type="password"
        class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-[#008659] focus:border-transparent outline-none transition"
        placeholder="請輸入目前的密碼"
      />
    </div>

    <div class="space-y-1">
      <label class="text-sm font-bold text-gray-700">新密碼</label>
      <input
        v-model="form.newPassword"
        type="password"
        class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-[#008659] focus:border-transparent outline-none transition"
        placeholder="請輸入新密碼"
      />
    </div>

    <div class="space-y-1">
      <label class="text-sm font-bold text-gray-700">確認新密碼</label>
      <input
        v-model="form.confirmPassword"
        type="password"
        class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-[#008659] focus:border-transparent outline-none transition"
        placeholder="請再次輸入新密碼"
      />
    </div>

    <div class="flex gap-3 mt-8 pt-2">
      <button
        @click="$emit('cancel')"
        class="flex-1 py-2.5 bg-gray-100 text-gray-600 rounded-xl font-bold hover:bg-gray-200 transition"
      >
        取消
      </button>
      <button
        @click="handleSubmit"
        class="flex-1 py-2.5 bg-[#008659] text-white rounded-xl font-bold hover:bg-[#1e4a36] shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="!isValid"
      >
        確認修改
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'

const emit = defineEmits<{
  (e: 'cancel'): void
  (e: 'submit', data: any): void
}>()

const form = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const isValid = computed(() => {
  return (
    form.oldPassword &&
    form.newPassword &&
    form.confirmPassword &&
    form.newPassword === form.confirmPassword
  )
})

const handleSubmit = () => {
  if (form.newPassword !== form.confirmPassword) {
    alert('兩次新密碼輸入不一致')
    return
  }
  emit('submit', { ...form })
  // 清空
  form.oldPassword = ''
  form.newPassword = ''
  form.confirmPassword = ''
}
</script>
