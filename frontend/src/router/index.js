// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import UserTable from '@/components/UserTable.vue'
import UserDetail from '@/views/UserDetail.vue'

const routes = [
  { path: '/', component: UserTable },
  { path: '/users/:id', component: UserDetail, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
