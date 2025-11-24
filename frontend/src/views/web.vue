<template>
  <div class="min-h-screen flex flex-col bg-white font-sans relative">
    <header class="sticky top-0 z-50 shadow-md bg-white">
      <MeetroHeader />
    </header>

    <main class="flex-grow w-full relative">
      <RouterView />
    </main>

    <footer class="w-full bg-[#5e5e5e] py-4 shadow-inner z-10 relative">
      <div class="container mx-auto px-4 text-center text-sm text-white">
        <MeetroFooter />
      </div>
    </footer>

    <FloatingChat v-if="isUser" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterView } from 'vue-router'
import { useRoleStore } from '@/stores/modules/useRole'
import MeetroHeader from '@/components/shared/MeetroHeader.vue'
import MeetroFooter from '@/components/shared/MeetroFooter.vue'
import FloatingChat from '@/components/shared/FloatingChat.vue'

const roleStore = useRoleStore()
const isUser = computed(() => roleStore.isUser)
</script>
