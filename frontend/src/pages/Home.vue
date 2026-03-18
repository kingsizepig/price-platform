<template>
  <div class="home">
    <van-search
      v-model="keyword"
      placeholder="搜索商品..."
      @search="onSearch"
      :show-action="true"
      action-text="搜索"
    />
    
    <van-tabs v-model:active="activeTab">
      <van-tab title="分类导航">
        <div class="category-grid">
          <div
            v-for="cat in rootCategories"
            :key="cat.id"
            class="category-item"
            @click="goCategory(cat.id)"
          >
            <span class="category-name">{{ cat.name }}</span>
          </div>
        </div>
      </van-tab>
      <van-tab title="热门商品">
        <!-- 热门商品可以后续实现，这里先占位 -->
        <div class="empty-tip">热门商品功能开发中...</div>
      </van-tab>
    </van-tabs>

    <van-tabbar v-model="activeTabbar" @change="onTabbarChange">
      <van-tabbar-item icon="home-o">首页</van-tabbar-item>
      <van-tabbar-item icon="star-o">自选</van-tabbar-item>
      <van-tabbar-item icon="user-o">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'
import { showToast } from 'vant'

const router = useRouter()
const keyword = ref('')
const activeTab = ref(0)
const activeTabbar = ref(0)
const rootCategories = ref([])

const onSearch = () => {
  if (!keyword.value.trim()) {
    showToast('请输入关键词')
    return
  }
  router.push({ name: '分类列表', params: { id: 0 } })
}

const goCategory = (id) => {
  router.push({ name: '分类列表', params: { id } })
}

const onTabbarChange = (index) => {
  if (index === 1) {
    router.push({ name: '我的自选' })
  } else if (index === 2) {
    router.push({ name: '个人中心' })
  }
}

const loadCategories = async () => {
  try {
    const res = await api.productCategories()
    if (res.data.code === 0) {
      rootCategories.value = res.data.data.filter(c => c.level === 1)
    }
  } catch (e) {
    showToast('加载分类失败')
  }
}

onMounted(() => {
  loadCategories()
  // 初始化用户ID，如果没有则创建
  if (!localStorage.getItem('user_id')) {
    const randomName = 'user_' + Math.random().toString(36).slice(2, 8)
    api.createUser(randomName).then(res => {
      if (res.data.code === 0) {
        localStorage.setItem('user_id', res.data.data.id)
      }
    })
  }
})
</script>

<style lang="less" scoped>
.home {
  min-height: 100vh;
  padding-bottom: 60px;
}

.category-grid {
  padding: 10px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.category-item {
  background: white;
  border-radius: 8px;
  padding: 20px 10px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  
  .category-name {
    font-size: 15px;
    color: #333;
  }
}

.empty-tip {
  text-align: center;
  padding: 40px 0;
  color: #999;
  font-size: 14px;
}
</style>
