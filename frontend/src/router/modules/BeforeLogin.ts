import { RouteModel } from '.'
import { RouteRecordRaw } from 'vue-router'

const routes = new RouteModel(null)
const beforeLoginRoutes: RouteRecordRaw[] = [
  routes.login(),
  routes.register(),
  routes.forgetPassword(),
  routes.home(),
]

export default beforeLoginRoutes
