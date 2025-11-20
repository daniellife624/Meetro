import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLoadingStore = defineStore('loading', () => {
  // --- State ---
  const isLoading = ref(false)
  const loadingText = ref('載入中...')

  // --- Actions ---
  /**
   * 設定 Loading 狀態
   * @param status 是否顯示 Loading
   * @param text Loading 顯示文字 (選填)
   */
  function setLoading(status: boolean, text?: string) {
    isLoading.value = status
    if (text) {
      loadingText.value = text
    }
  }

  // --- Return (必須回傳，外部才拿得到) ---
  return {
    isLoading,
    loadingText,
    setLoading, // 這裡一定要回傳，Router 才能呼叫 loadingStore.setLoading
  }
})
