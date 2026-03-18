import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
})

// 请求拦截器，添加用户ID
api.interceptors.request.use(config => {
  const userId = localStorage.getItem('user_id')
  if (userId) {
    config.headers['X-User-ID'] = userId
  }
  return config
})

export default {
  // 商品
  productSearch: (keyword, page = 1) => 
    api.get('/product/search', { params: { keyword, page, page_size: 20 } }),
  
  productDetail: productId => 
    api.get(`/product/detail/${productId}`),
  
  productCategories: () => 
    api.get('/product/categories'),
  
  addFavorite: productId => 
    api.post('/product/favorite/add', { product_id: productId }),
  
  removeFavorite: productId => 
    api.post('/product/favorite/remove', { product_id: productId }),
  
  listFavorites: () => 
    api.get('/product/favorite/list'),
  
  listByCategory: (categoryId, page = 1) => 
    api.get('/product/list', { params: { category_id: categoryId, page, page_size: 20 } }),
  
  // 价格
  createPrice: data => 
    api.post('/price/create', data),
  
  updatePrice: (priceId, data) => 
    api.post(`/price/update/${priceId}`, data),
  
  deletePrice: priceId => 
    api.post(`/price/delete/${priceId}`),
  
  listMyPrices: (page = 1) => 
    api.get('/price/user/my', { params: { page, page_size: 20 } }),
  
  // 用户
  getUserInfo: () => 
    api.get('/user/info'),
  
  createUser: username => 
    api.post('/user/create', { username }),
  
  getLevels: () => 
    api.get('/user/levels'),
}
