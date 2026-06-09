import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'
import ui from '@nuxt/ui/vue-plugin'

import App from './App.vue'
import './style.css'
import { router } from './common/router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ui)
app.use(VueQueryPlugin)

app.mount('#app')
