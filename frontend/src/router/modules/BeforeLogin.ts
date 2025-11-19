import { RouteModel } from './index' // 確保從 index.ts 匯入 RouteModel
import { RouteRecordRaw } from 'vue-router'

const routes = new RouteModel(null) // null 代表 'beforeLogin' 角色
const beforeLoginRoutes: RouteRecordRaw[] = [
  routes.home(), // index
  routes.login(), // login
  routes.register(),
  routes.forgetPassword(),
  routes.members(), // members
]

export default beforeLoginRoutes
