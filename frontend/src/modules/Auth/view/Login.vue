<script setup lang="ts">
import { ref } from 'vue';
import { Mail } from 'lucide-vue-next';

const username = ref('');

</script>

<template>
    <div class="h-screen w-screen flex items-center justify-center">
        <div class="flex flex-col gap-y-6 items-center border-2 border-primary-content rounded-md w-md">
            <h1 class="text-success">Login</h1>
            <UFormField label="Email">
                <UInput placeholder="Enter your email" color="primary" />
            </UFormField>
        </div>
    </div>
</template>