import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import ProductList from '../views/ProductList.vue'
import CategoryList from '../views/CategoryList.vue'
import UserList from '../views/UserList.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: '数据概览' }
  },
  {
    path: '/products',
    name: 'Products',
    component: ProductList,
    meta: { title: '商品管理' }
  },
  {
    path: '/categories',
    name: 'Categories',
    component: CategoryList,
    meta: { title: '分类管理' }
  },
  {
    path: '/users',
    name: 'Users',
    component: UserList,
    meta: { title: '用户管理' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
