/**
 * @description 暫時性的 Vue Composable (Stub) for handling cookie operations.
 * 由於 'js-cookie' 匯入失敗，暫時使用空操作 (No-op) 函數。
 */
const useCookies = () => {
  // 設置 Cookie (暫時無操作)
  const set = (key: string, value: string, remember: boolean = true) => {
    // 輸出警告，讓你知道這個功能目前被禁用
    console.warn(
      `[STUB] Cookie set called: ${key}=${value}, remember=${remember}. (Functionality disabled)`,
    )
  }

  // 取得 Cookie 值 (暫時回傳 undefined)
  const get = (key: string): string | undefined => {
    // 為了讓 Store 邏輯在註解期間繼續運行，我們暫時回傳 undefined
    return undefined
  }

  // 刪除 Cookie (暫時無操作)
  const remove = (key: string) => {
    console.warn(`[STUB] Cookie remove called: ${key}. (Functionality disabled)`)
  }

  return { set, get, remove }
}

export default useCookies
