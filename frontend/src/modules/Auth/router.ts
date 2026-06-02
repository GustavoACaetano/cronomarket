import type { RouteRecordRaw } from 'vue-router'


const routes: RouteRecordRaw[] = [
  {
    path: '',
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/modules/Auth/view/Login.vue'),
      },
      {
        path: 'cadastro',
        name: 'Cadastro',
        component: () => import('@/modules/Auth/view/Cadastro.vue'),
      },
    ],
  },
]

export default routes