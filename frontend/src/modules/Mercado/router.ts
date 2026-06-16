import type { RouteRecordRaw } from 'vue-router'
import LayoutBase from '@/layouts/LayoutBase.vue'

const routes: RouteRecordRaw[] = [
  {
    path: 'mercados',
    component: LayoutBase,
    children: [
      {
        path: 'home',
        name: 'PaginaInicial',
        component: () => import('@/modules/Mercado/view/PaginaInicial.vue'),
      },
      {
        path: 'criar',
        name: 'CriarMercado',
        component: () => import('@/modules/Mercado/view/CriarMercado.vue'),
      },
    ],
  },
]

export default routes