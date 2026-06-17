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
      {
        path: ':id',
        name: 'DetalhesMercado',
        component: () => import('@/modules/Mercado/view/DetalhesMercado.vue'),
      },
      {
        path: 'carteira',
        name: 'Carteira',
        component: () => import('@/modules/Mercado/view/Carteira.vue'),
      },
      {
        path: 'admin-dashboard',
        name: 'DashboardAdmin',
        component: () => import('@/modules/Mercado/view/DashboardAdmin.vue'),
      },
    ],
  },
]

export default routes