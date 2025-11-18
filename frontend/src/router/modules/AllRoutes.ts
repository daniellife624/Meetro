import { RouteRecordRaw } from 'vue-router'
import { RouteModel } from '.'

const routes = new RouteModel(null, true)
export const allRoutes: RouteRecordRaw[] = Object.values(routes).reduce((acc, route) => {
  if (typeof route === 'function') acc.push(route())
  return acc
}, [])
