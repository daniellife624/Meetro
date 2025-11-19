import { computed } from 'vue'
import { useStore } from '@/stores'
import { useRouter } from 'vue-router'

export const useRouters = () => {
  const router = useRouter()
  const id = computed(() => router.currentRoute.value.params.id as unknown as number)
  return { router, id }
}

export const useRole = () => {
  const store = useStore()
  const role = computed(() => store.role)
  const isLogin = computed(() => store.isLogin)
  return {
    role,
    isLogin,
    apiRole: computed(() => store.apiRole),
    store,
    isUserRole: computed(() => role.value === 'user'),
  }
}

export const useRouterTab = <T>({ tabs, firstTab = undefined }: { tabs: T[]; firstTab?: T }) => {
  const router = useRouter()
  const routeName = computed(() => router.currentRoute.value.name)
  const routerPath = computed(() => router.currentRoute.value.path)
  const routeQuery = computed(() => router.currentRoute.value.query)
  firstTab = firstTab || tabs[0]
  const curTab = computed({
    get: () => (router.currentRoute.value.query?.tab || firstTab) as T,
    set: (tab: any) => {
      router.replace(
        routeName.value
          ? { name: routeName.value, query: { ...routeQuery.value, tab } }
          : { path: routerPath.value, query: { ...routeQuery.value, tab } },
      )
    },
  })

  function changeTab(tab: T) {
    curTab.value = tab
  }

  return { router, routerPath, routeName, routeQuery, curTab, changeTab }
}
