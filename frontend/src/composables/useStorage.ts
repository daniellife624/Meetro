type StorageType = 'sessionStorage' | 'localStorage'

const useStorage = (type: StorageType) => {
  const set = (key: string, value: string) => {
    if (type === 'sessionStorage') {
      sessionStorage.setItem(key, value)
      return
    }
    localStorage.setItem(key, value)
  }

  const get = (key: string) =>
    type === 'sessionStorage' ? sessionStorage.getItem(key) : localStorage.getItem(key)

  const clear = (key: string) => {
    if (type === 'sessionStorage') {
      sessionStorage.removeItem(key)
      return
    }
    localStorage.removeItem(key)
  }

  const clearAll = () => {
    if (type === 'sessionStorage') {
      sessionStorage.clear()
      return
    }
    localStorage.clear()
  }

  return {
    get,
    set,
    clear,
    clearAll,
  }
}

export default useStorage
