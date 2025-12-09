<template>
  <div class="min-h-full w-full bg-white p-8 font-sans pb-20">
    <div
      class="w-full border border-gray-400 rounded-[20px] p-3 mb-12 flex flex-row items-center space-x-4 shadow-sm"
    >
      <div
        class="bg-[#008659] text-white font-bold text-xl px-10 py-3 rounded-[10px] text-center shadow-md whitespace-nowrap flex-shrink-0"
      >
        模擬參數表
      </div>

      <div
        class="flex-grow border border-[#008659] rounded-[10px] px-6 py-3 flex items-center bg-white text-lg font-bold text-gray-800 tracking-wide shadow-inner overflow-hidden"
      >
        <span class="truncate">參數 ： {{ parameterListString }}</span>
      </div>
    </div>

    <div class="w-full mb-16">
      <div class="flex space-x-5 overflow-x-auto pb-8 px-2 scrollbar-hide items-stretch">
        <VariableCard
          v-for="(variable, index) in variables"
          :key="variable.id"
          :title="`參數${index + 1}：${variable.name}`"
          :rule="variable.rule"
          v-model="variable.weight"
          @remove="removeVariable(index)"
        />
        <AddVariableCard @add="addNewVariable" class="min-h-[420px]" />
      </div>
    </div>

    <div class="flex items-start gap-6 w-full">
      <div class="relative w-3/4">
        <div
          class="w-full h-20 border-2 rounded-[14px] flex items-center justify-between px-4 md:px-8 transition-colors duration-300 shadow-sm bg-white"
          :class="isOverLimit ? 'border-red-500 bg-red-50' : 'border-gray-400'"
        >
          <span
            class="text-xl md:text-2xl font-extrabold tracking-widest text-gray-800 truncate mr-2"
          >
            目前累計總權重 :
          </span>

          <div class="text-3xl md:text-4xl font-black flex items-baseline flex-shrink-0">
            <span :class="isOverLimit ? 'text-red-600' : 'text-gray-800'">{{ totalWeight }}</span>
            <span class="text-xl md:text-2xl ml-1 text-gray-500 font-bold">%</span>
          </div>
        </div>

        <div
          v-if="isOverLimit"
          class="absolute top-full left-0 mt-2 flex items-center text-red-500 font-bold animate-pulse text-sm md:text-base"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 mr-1"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clip-rule="evenodd"
            />
          </svg>
          錯誤：超過 100%
        </div>
      </div>

      <button
        @click="handleSave"
        :disabled="isOverLimit"
        class="w-1/4 h-20 bg-[#008659] text-white text-lg md:text-xl font-bold rounded-[14px] shadow-lg hover:bg-[#006d48] disabled:bg-gray-400 disabled:cursor-not-allowed transition-all transform active:scale-95 flex items-center justify-center flex-shrink-0 whitespace-nowrap"
      >
        確定修改
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import VariableCard from '@/components/bcms/VariableCard.vue'
import AddVariableCard from '@/components/bcms/AddVariableCard.vue'
import request from '@/utils/request'

interface Variable {
  id: number
  name: string
  weight: number
  rule: string // 對應 SystemVariable.rule_desc
}

// 變數初始化為空，等待 API 載入
const variables = ref<Variable[]>([])

// --- API 載入 ---
const fetchConfig = async () => {
  try {
    // 呼叫 GET /api/bcms/config
    const res: any[] = await request.get('/api/bcms/config')

    // 後端返回的 rule_desc 在前端命名為 rule
    variables.value = res.map((v) => ({
      id: v.id,
      name: v.name,
      weight: v.weight,
      rule: v.rule,
    }))

    console.log('BCMS 配置載入成功:', variables.value)
  } catch (error) {
    console.error('BCMS 配置載入失敗:', error)
    // 如果載入失敗，給予一個預設值，確保介面不崩潰
    variables.value = [
      { id: 1, name: '歷史滿意度', weight: 50, rule: '無法載入後端數據，使用預設值。' },
      { id: 2, name: '天氣影響', weight: 30, rule: '無法載入後端數據，使用預設值。' },
      { id: 3, name: '地點熱門度', weight: 20, rule: '無法載入後端數據，使用預設值。' },
    ]
    alert('無法載入 BCMS 參數，請檢查後端服務和初始化數據。')
  }
}

onMounted(() => {
  fetchConfig()
})

// --- Computed ---
const parameterListString = computed(() => variables.value.map((v) => v.name).join(' ｜ '))
const totalWeight = computed(() => variables.value.reduce((sum, item) => sum + item.weight, 0))
const isOverLimit = computed(() => totalWeight.value > 100)

// --- Actions ---

const addNewVariable = () => {
  const name = prompt('請輸入新參數名稱：')
  if (name) {
    variables.value.push({
      id: Date.now(),
      name: name,
      weight: 0,
      rule: '請設定此參數的相關規則...',
    })
  }
}

const removeVariable = (index: number) => {
  if (confirm('確定要移除這個參數嗎？')) variables.value.splice(index, 1)
}

const handleSave = async () => {
  if (totalWeight.value !== 100) {
    alert(`目前總權重為 ${totalWeight.value}%，必須剛好等於 100% 才能儲存！`)
    return
  }

  const dataToSend = variables.value.map((v) => ({
    name: v.name,
    weight: v.weight,
    rule: v.rule,
  }))

  try {
    // 呼叫 POST /api/bcms/config/save
    await request.post('/api/bcms/config/save', dataToSend)
    alert('參數設定已成功更新並保存！')
    // 保存成功後重新載入，以確保數據 ID 正確
    await fetchConfig()
  } catch (error: any) {
    console.error('保存 BCMS 配置失敗:', error)
    alert(`保存失敗：${error.detail || error.message || '未知錯誤'}`)
  }
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
