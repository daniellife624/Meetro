import { defineStore } from 'pinia'

// 這是為了解決構建錯誤而創建的最小 Pinia Store 佔位符。
// 它導出了一個名為 "useLoadingStore" 的函式，供其他部分引用。

export const useLoadingStore = defineStore('loading', {
  // 狀態 (State) - 定義儲存的資料
  state: () => ({
    isLoading: false as boolean,
    loadingMessage: '' as string,
  }),

  // 行為 (Actions) - 定義修改狀態的方法
  actions: {
    startLoading(message = '正在加載...') {
      this.isLoading = true
      this.loadingMessage = message
    },
    stopLoading() {
      this.isLoading = false
      this.loadingMessage = ''
    },
  },

  // 計算屬性 (Getters) - 定義派生狀態
  getters: {
    getLoadingStatus: (state) => state.isLoading,
  },
})
