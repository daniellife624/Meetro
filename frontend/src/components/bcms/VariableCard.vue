<template>
  <div
    class="min-w-[280px] w-[280px] min-h-[400px] bg-white border-2 border-gray-300 rounded-2xl p-6 flex flex-col items-center shadow-sm hover:shadow-md transition-shadow relative flex-shrink-0"
  >
    <button
      @click="$emit('remove')"
      class="absolute top-3 right-3 text-gray-300 hover:text-red-500 transition"
      title="移除此參數"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
          clip-rule="evenodd"
        />
      </svg>
    </button>

    <div
      class="bg-[#666666] text-white px-4 py-3 text-center font-bold text-lg rounded-md mb-8 tracking-wider shadow-sm"
    >
      {{ title }}
    </div>

    <div class="relative w-[90%] mb-8">
      <input
        type="number"
        :value="modelValue"
        @input="updateValue"
        class="w-full pl-4 pr-10 py-3 text-center text-gray-700 border-2 border-gray-300 rounded-full focus:border-[#008659] focus:ring-2 focus:ring-green-100 outline-none transition font-bold text-xl placeholder-gray-300"
        placeholder="輸入權重"
        min="0"
        max="100"
      />
      <span
        class="absolute right-5 top-1/2 transform -translate-y-1/2 text-gray-500 font-bold text-lg"
        >%</span
      >
    </div>

    <div class="w-full text-center space-y-3 flex-grow flex flex-col">
      <p class="font-bold text-gray-800 text-base">參數設定規則 :</p>
      <p class="text-xs text-gray-500 leading-loose break-words px-2 tracking-wide">
        {{ rule }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  title: string
  modelValue: number
  rule: string
}>()

const emit = defineEmits(['update:modelValue', 'remove'])

const updateValue = (event: Event) => {
  const target = event.target as HTMLInputElement
  let val = parseInt(target.value)
  if (isNaN(val) || val < 0) val = 0
  emit('update:modelValue', val)
}
</script>
