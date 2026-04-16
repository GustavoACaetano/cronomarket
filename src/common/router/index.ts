import { createRouter, createWebHistory } from 'vue-router'
import landingPageRoutes from '@/modules/LandingPage/router'


export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
     {
      path: '/',
      children: [
        ...landingPageRoutes,
      ],
    },
  ],
})
