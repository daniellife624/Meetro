// Header 選項
export interface NavItem {
  name: string
  icon: string
  type: 'router' | 'grouped'
  routeName?: string
  count?: number
  children?: NavItem[]
}
