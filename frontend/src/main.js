import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import Vant from 'vant'
import 'vant/lib/index.css'
import App from './App.vue'
import routes from './routes'
import './style.less'

const app = createApp(App)
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

app.use(Vant)
app.use(router)
app.mount('#app')
