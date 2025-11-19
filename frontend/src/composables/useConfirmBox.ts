import ConfirmBoxVue from '@/components/web/PopupBox/ConfirmBox.vue'
import { h, render, VNode } from 'vue'

export type PopupType = 'normal' | 'error'

interface ConfirmParams {
  msg: string
  title: string
  type?: PopupType
  cancelText?: string
  confirmText?: string
}

export interface ResolveFun {
  (v: boolean): void
}

export interface RejectFun {
  (reason?: any): void
}

function createConfirmBox(
  resolve: ResolveFun,
  reject: RejectFun,
  { msg, type, title, cancelText, confirmText }: ConfirmParams,
): VNode {
  const id = 'confirm-box'

  const _container = document.querySelector(`#${id}`)
  const container = _container || document.createElement('div')
  container.setAttribute('id', id)
  // 銷毀彈窗
  const destroy = () => {
    render(null, container)
  }

  const vNode = h(ConfirmBoxVue, {
    message: msg,
    title: title,
    type: type,
    cancelText: cancelText,
    confirmText: confirmText,
    confirmCallback: () => {
      resolve(true)
      destroy()
    },
    cancelCallback: () => {
      destroy()
      reject()
    },
  })

  render(vNode, container)
  document.body.appendChild(container)

  return vNode
}

export function $confirm({
  msg,
  title,
  type = undefined,
  cancelText = undefined,
  confirmText = undefined,
}: ConfirmParams) {
  return new Promise<boolean>((resolve, reject) => {
    createConfirmBox(resolve, reject, { msg, title, type, cancelText, confirmText })
  })
}
