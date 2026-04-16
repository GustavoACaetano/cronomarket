import type { RouteRecordRaw } from 'vue-router'


const routes: RouteRecordRaw[] = [
  {
    path: '',
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