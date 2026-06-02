<script setup lang="ts">
import { ref } from 'vue';
import { Mail } from 'lucide-vue-next';

const username = ref('');

</script>

<template>
    <div class="h-screen w-screen flex items-center justify-center">
        <div class="flex flex-col gap-y-6 items-center border-2 border-primary-content rounded-md w-md">
            <h1 class="text-black">Login</h1>
            <div class="flex flex-col items-center gap-y-4 w-full">
                <form class="fieldset w-3/4 px-6">
                    <div class="flex flex-col gap-y-4">
                        <fieldset class="fieldset">
                            <label class="label">Email</label>
                            <input type="email" class="input validator" placeholder="Email" required />
                            <p class="validator-hint hidden">Required</p>
                        </fieldset>

                        <label class="fieldset">
                            <span class="label">Password</span>
                            <input type="password" class="input validator" placeholder="Password" required />
                            <span class="validator-hint hidden">Required</span>
                        </label>
                    </div>
                    <div class="flex justify-end">
                        <span>Não tem conta? <a href="/cadastro" class="link">Cadastre-se</a></span>
                    </div>

                    <div class="flex flex-row justify-end items-center mt-4">
                        <button class="btn btn-ghost" type="reset">Reset</button>
                        <button class="btn btn-primary" type="submit">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>