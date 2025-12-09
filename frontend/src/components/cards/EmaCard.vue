<template>
  <div
    class="filter drop-shadow-md hover:drop-shadow-xl transition-all duration-300 mb-6 group break-inside-avoid"
  >
    <div
      class="relative bg-[#B47F2E] text-gray-800 w-full overflow-hidden"
      style="clip-path: polygon(50% 0%, 100% 12%, 100% 100%, 0% 100%, 0% 12%); padding-top: 15%"
    >
      <div
        class="absolute top-2 left-1/2 transform -translate-x-1/2 w-1.5 h-12 bg-white rounded-full z-20 shadow-sm"
      ></div>
      <div
        class="absolute top-8 left-1/2 transform -translate-x-1/2 w-4 h-4 bg-white rounded-full z-20 border-2 border-white"
      ></div>

      <div class="relative h-40 mx-4 mt-2 rounded-lg overflow-hidden border-2 border-[#e6dcca]">
        <img
          :src="ema.photoUrl || 'https://placehold.co/400x300/e2e8f0/a0aec0?text=No+Photo'"
          alt="Ema Photo"
          class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
        />

        <div
          class="absolute bottom-1 left-1 bg-black/60 text-white text-md px-2 py-2 rounded backdrop-blur-sm font-medium tracking-wide truncate max-w-[85%]"
        >
          {{ ema.location }}
        </div>
      </div>

      <div class="p-5">
        <div
          class="absolute top-0 left-0 w-full h-full pointer-events-none opacity-10"
          style="
            background-image: repeating-linear-gradient(
              45deg,
              #bfa76f 0,
              #bfa76f 1px,
              transparent 0,
              transparent 50%
            );
            background-size: 20px 20px;
          "
        ></div>

        <p class="text-white text-sm leading-relaxed mb-4 font-medium relative z-10 min-h-[3rem]">
          {{ ema.content }}
        </p>

        <div class="flex items-center justify-between pt-5 border-t border-[#e6dcca] relative z-10">
          <div class="flex items-center space-x-2">
            <div
              class="w-6 h-6 rounded-full bg-white border border-gray-200 overflow-hidden flex items-center justify-center"
            >
              <SvgItem name="user" size="4" class="text-gray-400" />
            </div>
            <span class="text-xs text-white font-bold">{{ ema.userName }}</span>
          </div>
          <span class="text-[10px] text-white">{{ ema.date }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SvgItem from '@/components/icons/SvgItem.vue'

export interface EmaItem {
  id: number
  userName: string
  location: string
  content: string
  photoUrl: string
  date: string
}

defineProps<{
  ema: EmaItem
}>()
</script>

<style scoped></style>
