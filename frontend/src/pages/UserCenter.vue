<template>
  <div class="user-center">
    <van-cell-group>
      <van-cell title="用户名" :value="userInfo.username" />
      <van-cell title="当前等级" :value="userInfo.level_name" />
      <van-cell title="当前积分" :value="userInfo.integral" />
      <van-cell title="价格权重" :value="userInfo.weight" />
    </van-cell-group>

    <div class="menu-list">
      <van-cell is-link title="我的录入" @click="goTo('/records')" />
      <van-cell is-link title="我的自选" @click="goTo('/favorites')" />
    </div>

    <div class="level-info">
      <h3>等级说明</h3>
      <div v-for="level in levels" :key="level.level" class="level-item">
        <span>{{ level.level }} {{ level.name }}</span>
        <span>积分 {{ level.min_points }}+，权重 {{ level.weight }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()
const userInfo = ref({
  username: '',
  integral: 0,
  level: 1,
  level_name: '',
  weight: 0.5,
})
const levels = ref([])

const goTo = (path) => {
  router.push(path)
}

const loadData = async () => {
  try {
    const [userRes, levelRes] = await Promise.all([
      api.getUserInfo(),
      api.getLevels(),
    ])
    
    if (userRes.data.code === 0) {
      userInfo.value = userRes.data.data
    }
    if (levelRes.data.code === 0) {
      levels.value = levelRes.data.data
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="less" scoped>
.user-center {
  background: #f7f8fa;
  min-height: 100vh;
  
  .menu-list {
    margin-top: 10px;
    background: white;
  }
  
  .level-info {
    margin: 10px;
    background: white;
    border-radius: 8px;
    padding: 15px;
    
    h3 {
      font-size: 15px;
      color: #333;
      margin-bottom: 10px;
    }
    
    .level-item {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid #f0f0f0;
      
      &:last-child {
        border-bottom: none;
      }
      
      span:first-child {
        color: #333;
      }
      
      span:last-child {
        color: #666;
        font-size: 13px;
      }
    }
  }
}
</style>
