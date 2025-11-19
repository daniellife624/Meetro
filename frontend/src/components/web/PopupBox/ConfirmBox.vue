<template>
  <PopupBoxLayout
    :title="title"
    :type="type"
    :cancel-callback="cancelCallback"
    :confirm-callback="confirmCallback"
    :confirm-text="confirmText"
    :cancel-text="cancelText"
  >
    {{ message }}
  </PopupBoxLayout>
</template>

<script setup lang="ts">
import PopupBoxLayout from '@/components/PopupBox/PopupBoxLayout.vue'
import { PopupType } from '@/composables/useConfirmBox'

interface Props {
  message: string
  title: string
  cancelCallback: () => void
  confirmCallback: () => void
  type?: PopupType
  cancelText?: string
  confirmText?: string
}

const props = withDefaults(defineProps<Props>(), {})
</script>

<style lang="scss"></style>
