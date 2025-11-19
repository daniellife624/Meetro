<template>
  <div class="h-full flex flex-col bg-white">
    <header class="sticky top-0 z-50 shadow-md bg-white">
      <MeetroHeader />
    </header>

    <main class="flex-grow container w-full h-full bg-black">
      <RouterView />
    </main>

    <!-- 3. 底部 Footer 區域 (高度固定) -->
    <footer class="w-full bg-[#5e5e5e] py-4 shadow-inner">
      <div class="container mx-auto px-4 text-center text-sm text-white">
        <MeetroFooter />
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import MeetroHeader from '@/components/shared/MeetroHeader.vue'
import MeetroFooter from '@/components/shared/MeetroFooter.vue'
</script>
