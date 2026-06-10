import { createRouter, createWebHistory } from 'vue-router'
import landingPageRoutes from '@/modules/LandingPage/router'
import authRoutes from '@/modules/Auth/router'

const hasStoredUser = () => {
  const storedUser = localStorage.getItem('cronomarket_user')

  if (!storedUser) {
    return false
  }

  try {
    const user = JSON.parse(storedUser)

    return (
      user &&
      typeof user === 'object' &&
      'id' in user &&
      'username' in user &&
      'email' in user &&
      'usuario_id' in user
    )
  } catch {
    return false
  }
}


export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login',
      children: [
        ...authRoutes,
        ...landingPageRoutes,
      ],
    },
  ],
})

router.beforeEach((to) => {
  if (to.path === '/login' && hasStoredUser()) {
    return '/landing-page'
  }
  if (to.path === '/cadastro' && hasStoredUser()) {
    return '/landing-page'
  }

  return true
})
