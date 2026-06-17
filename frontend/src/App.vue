<script setup lang="ts">
import { pt_br } from '@nuxt/ui/locale'
import { useColorMode } from '@vueuse/core'

const colorMode = useColorMode()
colorMode.value = 'light'
</script>

<template>
  <UApp :locale="pt_br">
    <RouterView />
  </UApp>
</template>
