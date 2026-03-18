import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000/api'

const request = axios.create({
  baseURL: API_BASE,
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(config => {
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器
request.interceptors.response.use(response => {
  const res = response.data
  if (res.code !== 0) {
    console.error(res.message || '请求错误')
    return Promise.reject(res)
  }
  return res.data
}, error => {
  console.error(error.message)
  return Promise.reject(error)
})

// 商品管理API
export const productApi = {
  list: (params) => request.get('/products', { params }),
  detail: (id) => request.get(`/products/${id}`),
  create: (data) => request.post('/products', data),
  update: (id, data) => request.put(`/products/${id}`, data),
  delete: (id) => request.delete(`/products/${id}`),
}

// 分类管理API
export const categoryApi = {
  list: () => request.get('/categories'),
  create: (data) => request.post('/categories', data),
  update: (id, data) => request.put(`/categories/${id}`, data),
  delete: (id) => request.delete(`/categories/${id}`),
}

// 用户管理API
export const userApi = {
  list: (params) => request.get('/users', { params }),
  update: (id, data) => request.put(`/users/${id}`, data),
}

export default request
