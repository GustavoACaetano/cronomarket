<script lang="ts" setup>
import AppHeader from './components/AppHeader.vue';
</script>

<template>
    <div class="flex flex-col flex-1 h-full overflow-hidden">
      <AppHeader  />

      <main class="flex-1 overflow-y-auto overflow-x-hidden">
        <div class="w-full px-4 md:px-8 py-8">
          <router-view />
        </div>
      </main>
    </div>
</template>