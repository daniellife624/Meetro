<template>
  <div class="w-full h-full">
    <RouterView />
    <GlobalLoadingOverlay />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import GlobalLoadingOverlay from '@/components/shared/GlobalLoadingOverlay.vue'
</script>

<style scoped></style>
