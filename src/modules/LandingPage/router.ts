import type { RouteRecordRaw } from 'vue-router'


const routes: RouteRecordRaw[] = [
  {
    path: '/landing-page',
    children: [
      {
        path: '',
        name: 'LandingPage',
        component: () => import('@/modules/LandingPage/view/index.vue'),
      },
    ],
  },
]

export default routes