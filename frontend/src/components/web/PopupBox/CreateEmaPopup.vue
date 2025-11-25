<template>
  <div class="text-left">
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-bold text-gray-700 mb-1">探索地點</label>
        <input
          v-model="form.location"
          type="text"
          class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-[#008659] focus:border-transparent outline-none transition"
          placeholder="例如：公館夜市、寶藏巖..."
        />
      </div>

      <div>
        <label class="block text-sm font-bold text-gray-700 mb-1">心得隨筆</label>
        <textarea
          v-model="form.content"
          rows="4"
          class="w-full border border-gray-300 rounded-lg p-2.5 resize-none focus:ring-2 focus:ring-[#008659] focus:border-transparent outline-none transition"
          placeholder="寫下你的心情..."
        ></textarea>
      </div>

      <div
        class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center text-gray-400 cursor-pointer hover:bg-gray-50 hover:border-[#008659] hover:text-[#008659] transition group relative overflow-hidden"
        @click="triggerFileInput"
      >
        <img
          v-if="previewImage"
          :src="previewImage"
          class="absolute inset-0 w-full h-full object-cover"
        />

        <div v-else class="flex flex-col items-center">
          <span class="text-2xl mb-2 group-hover:scale-110 transition-transform">+</span>
          <span class="text-sm font-medium">點擊上傳照片</span>
        </div>

        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleFileChange"
        />
      </div>
    </div>

    <div class="flex gap-3 mt-8">
      <button
        @click="$emit('cancel')"
        class="flex-1 py-2.5 bg-gray-100 text-gray-600 rounded-xl font-bold hover:bg-gray-200 transition"
      >
        取消
      </button>
      <button
        @click="handleSubmit"
        class="flex-1 py-2.5 bg-[#008659] text-white rounded-xl font-bold hover:bg-[#1e4a36] shadow-md hover:shadow-lg transition transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="!isValid"
      >
        發佈
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, ref } from 'vue'

const emit = defineEmits<{
  (e: 'cancel'): void
  (e: 'submit', data: { location: string; content: string; photoUrl: string }): void
}>()

const form = reactive({
  location: '',
  content: '',
  photoUrl: 'https://picsum.photos/400/300', // 預設圖
})

// 檔案上傳相關
const fileInput = ref<HTMLInputElement | null>(null)
const previewImage = ref<string | null>(null)

const isValid = computed(() => form.location.trim() !== '' && form.content.trim() !== '')

// 觸發選擇檔案
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 處理檔案變更
const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]

    // 建立預覽圖 URL
    const reader = new FileReader()
    reader.onload = (e) => {
      if (e.target?.result) {
        const result = e.target.result as string
        previewImage.value = result
        form.photoUrl = result // 在真實專案中，這裡應該是上傳後的 URL
      }
    }
    reader.readAsDataURL(file)
  }
}

const handleSubmit = () => {
  if (isValid.value) {
    emit('submit', { ...form })
    // 重置表單
    form.location = ''
    form.content = ''
    previewImage.value = null
  }
}
</script>
