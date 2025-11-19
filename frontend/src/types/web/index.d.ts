import { SvgType } from '@/composables/useSvg'

export type WebRole = 'user' | null
export type WebRoleAfterLogin = Exclude<WebRole, null>
export type ApiRole = 'user' | 'beforeLogin'
export type SendMessageType = 'message'
