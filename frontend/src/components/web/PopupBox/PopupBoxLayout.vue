<template>
  <CoverContainer :model-value="true" @click.self="cancelCallback" :teleport-to-body="false">
    <div
      v-is="useForm ? 'form' : 'div'"
      class="popup-box shadow shadow-sm"
      :id="id"
      @submit.prevent
    >
      <div class="body">
        <div class="title">
          <SvgItem :type="'circle-exclamation'" size="sm" class="text-blue-500"></SvgItem>
          {{ title }}
        </div>
        <div class="content">
          <slot></slot>
        </div>
      </div>
      <div class="btn-group">
        <button type="button" @click="cancelCallback">{{ cancelText }}</button>
        <button type="submit" @click="confirmCallback" :style="confirmBtnStyle">
          {{ confirmText }}
        </button>
      </div>
    </div>
  </CoverContainer>
</template>

<script setup lang="ts">
import CoverContainer from '@/components/container/CoverContainer.vue'
import SvgItem from '../SvgItem.vue'
import { ref, toRefs } from 'vue'
import { PopupType } from '@/composables/useConfirmBox'
import { computed } from '@vue/reactivity'

interface Props {
  title: string
  cancelCallback(): void
  confirmCallback(): void
  type?: PopupType
  cancelText?: string
  confirmText?: string
  useForm?: boolean
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'normal',
  cancelText: '取消',
  confirmText: '確認',
  useForm: false,
})

const { type } = toRefs(props)

const typeToColor: { [key in PopupType]: string } = {
  error: '#ef4444',
  normal: '#3b82f6',
}

const confirmBtnStyle = computed(() => {
  const btnColor = '#fff'
  const btnBg = typeToColor[type.value]

  const opacity = 0.7
  const colorA = Math.round(opacity * 255)
  const colorAHex = colorA.toString(16)

  const btnBgHover = btnBg + colorAHex
  return {
    '--confirm-btn-bg': btnBg,
    '--confirm-btn-bg-hover': btnBgHover,
    '--confirm-btn-color': btnColor,
  }
})
</script>

<style lang="scss">
.popup-box {
  background: #ffffff;
  width: min(95vw, 420px);
  min-height: 200px;
  border-radius: 4px;
  box-shadow: 0px 2px 8px 1px rgba(44, 110, 198, 0.06);

  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.5rem 1.25rem 1rem;
  .body {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    .title {
      font-weight: bold;
      font-size: 20px;
      line-height: 24px;
      text-align: left;
      color: #1e212c;
      margin-bottom: 0.75rem;
    }

    .content {
      overflow: auto;
      scrollbar-gutter: stable;
      font-size: 16px;
      line-height: 24px;
      text-align: left;
      color: #252d39;
      flex-grow: 1;
    }
  }

  .btn-group {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    button {
      height: 36px;
      padding: 8px 12px;
      min-width: 64px;
      font-weight: bold;
      font-size: 14px;
      border-radius: 0.125rem;
      &:nth-child(1) {
        background-color: #e0e0e0;
        &:hover {
          background-color: #e0e0e0c1;
        }
      }
      &:last-child {
        color: var(--confirm-btn-color);

        background-color: var(--confirm-btn-bg);
        &:hover {
          background-color: var(--confirm-btn-bg-hover);
        }
      }
    }
  }
}
</style>
