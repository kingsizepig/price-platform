import Home from './pages/Home.vue'
import ProductDetail from './pages/ProductDetail.vue'
import PriceAdd from './pages/PriceAdd.vue'
import MyFavorites from './pages/MyFavorites.vue'
import MyRecords from './pages/MyRecords.vue'
import UserCenter from './pages/UserCenter.vue'
import CategoryList from './pages/CategoryList.vue'

const routes = [
  { path: '/', name: '首页', component: Home },
  { path: '/category/:id', name: '分类列表', component: CategoryList },
  { path: '/product/:id', name: '商品详情', component: ProductDetail },
  { path: '/price/add/:productId', name: '录入价格', component: PriceAdd },
  { path: '/favorites', name: '我的自选', component: MyFavorites },
  { path: '/records', name: '我的录入', component: MyRecords },
  { path: '/user', name: '个人中心', component: UserCenter },
]

export default routes
