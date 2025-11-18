import { RouteRecordRaw } from 'vue-router'

export const notFoundRouteName = '404notFound'

export const notFoundRoute: RouteRecordRaw = {
  path: '/:pathMatch(.*)*',
  name: notFoundRouteName,
  component: () => import('@/views/404.vue'),
}
