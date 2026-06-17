import { createRouter, createWebHistory } from 'vue-router'
import landingPageRoutes from '@/modules/LandingPage/router'
import authRoutes from '@/modules/Auth/router'
import mercadosRoutes from '@/modules/Mercado/router'

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
      children: [
        ...authRoutes,
        ...landingPageRoutes,
        ...mercadosRoutes,
      ],
    },
  ],
})

router.beforeEach((to) => {
  const loggedIn = hasStoredUser()

  if (to.path === '/') {
    return loggedIn ? '/mercados/home' : '/landing-page'
  }

  // A logged in user should never access the landing page, login, or registration pages
  if (loggedIn && (to.path === '/landing-page' || to.path === '/login' || to.path === '/cadastro')) {
    return '/mercados/home'
  }

  return true
})
