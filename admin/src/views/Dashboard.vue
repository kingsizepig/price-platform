<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <div class="stat-num">{{ stats.products }}</div>
          <div class="stat-label">商品总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-num">{{ stats.records }}</div>
          <div class="stat-label">价格记录</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-num">{{ stats.categories }}</div>
          <div class="stat-label">分类数量</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-num">{{ stats.users }}</div>
          <div class="stat-label">用户数量</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../utils/api'

const stats = ref({
  products: 0,
  records: 0,
  categories: 0,
  users: 0
})

onMounted(async () => {
  // TODO: 调用统计接口获取数据
})
</script>

<style scoped>
.dashboard {
  padding: 20px 0;
}

.stat-num {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #999;
}
</style>
