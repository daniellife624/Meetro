// src/composables/useDynamicHeightTransition.ts
// 處理下拉選單高度變化的客製化過渡效果

interface UseDynamicHeightTransitionConfig {
  /**
   * @default "height .5s"
   * @param el - 元素
   * @param height - 元素預期的目標高度 (px)
   */
  enterTransition?(el: HTMLElement, height: number): void

  /**
   * @default "none" 預設會清除transition
   * @param el - 元素
   */
  afterEnter?(el: HTMLElement): void
}

/**
 * 提供用於 Vue <Transition> 的鉤子，以實現動態高度的平滑過渡。
 * @param config - 可選配置，用於自定義進入動畫和進入後的操作。
 */
export default function (config: UseDynamicHeightTransitionConfig = {}) {
  const {
    // 預設進入過渡：設置 height .5s 的過渡效果
    enterTransition = (el) => {
      el.style.transition = 'height .5s'
    },
    // 預設進入後：清除過渡，以便內容高度變化時不會觸發動畫
    afterEnter = (el) => {
      el.style.transition = 'none'
    },
  } = config

  /**
   * [before-enter, before-leave 鉤子] 元素進入前/離開前將高度設為0
   * @param el - 正在過渡的 HTML 元素
   */
  function handleBeforeEnter(el: Element) {
    if (!(el instanceof HTMLElement)) return
    el.style.height = '0'
  }

  /**
   * [enter 鉤子] 測量元素實際高度並開始進入動畫
   * @param el - 正在過渡的 HTML 元素
   * @returns
   */
  function handleEnter(el: Element) {
    if (!(el instanceof HTMLElement)) return

    // 1. 將高度設為 'auto' 以計算其真實高度
    el.style.height = 'auto'
    const height = el.clientHeight // 獲取元素內容的實際高度

    // 2. 立即將高度重設為 0
    el.style.height = '0'

    // 3. 請求下一幀動畫
    requestAnimationFrame(() => {
      // 4. 設置目標高度，並應用過渡樣式
      el.style.height = height + 'px'
      enterTransition(el, height)
    })
  }

  /**
   * [after-enter 鉤子] 動畫結束後清除 transition 和高度，允許內容自適應
   * @param el - 正在過渡的 HTML 元素
   */
  function handleAfterEnter(el: Element) {
    if (!(el instanceof HTMLElement)) return
    afterEnter(el)
    // 讓高度自適應，以免內容變化時被固定
    el.style.height = ''
  }

  /**
   * [leave 鉤子] 處理元素收合的動畫
   * @param el - 正在過渡的 HTML 元素
   * @param done - 動畫結束時必須呼叫的回調
   */
  function handleLeave(el: Element, done: () => void) {
    if (!(el instanceof HTMLElement)) return

    // 1. 設置初始高度為當前高度 (避免閃爍)
    el.style.height = el.clientHeight + 'px'

    // 2. 應用過渡樣式
    el.style.transition = 'height .5s'

    requestAnimationFrame(() => {
      // 3. 在下一幀將目標高度設為 0，開始收合動畫
      el.style.height = '0'
    })

    // 4. 監聽 transition 結束事件
    el.addEventListener(
      'transitionend',
      () => {
        el.style.height = ''
        el.style.transition = ''
        done()
      },
      { once: true },
    )
  }

  return {
    handleBeforeEnter,
    handleEnter,
    handleAfterEnter, // 雖然 NavButton 沒用，但保留完整的 Hook
    handleLeave, // 為了 NavButton 的收合而新增
  }
}
