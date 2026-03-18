<template>
  <el-container>
    <el-aside width="200px">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        router
      >
        <el-menu-item v-for="item in menuItems" :key="item.path">
          <template #title>
            <span>{{ item.meta.title }}</span>
          </template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <h2>商品价格分享平台 - 管理后台</h2>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const menuItems = [
  { path: '/dashboard', meta: { title: '数据概览' } },
  { path: '/products', meta: { title: '商品管理' } },
  { path: '/categories', meta: { title: '分类管理' } },
  { path: '/users', meta: { title: '用户管理' } },
]
</script>

<style scoped>
el-container {
  height: 100vh;
}

el-aside {
  background: #f5f5f5;
}

el-header {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  line-height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

el-header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.el-menu-vertical-demo {
  border-right: none;
}
</style>
